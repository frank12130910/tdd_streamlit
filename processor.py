import pandas as pd
from io import BytesIO

def process_excel(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)

    df_in = pd.read_excel(xls, sheet_name='来货数量')
    df_po = pd.read_excel(xls, sheet_name='PO数量')

    # 字段名称
    in_sku_col = 'sku'
    in_qty_col = '来货数量'
    in_customer_col = '客户'

    po_sku_col = 'SKU编码'
    po_qty_col = '数量'
    po_customer_col = '客户(新)'

    # ========= 客户校验 =========
    VALID_CUSTOMERS = {
        '亚马逊',
        '亚马逊-加拿大',
        '独立站',
        '美仓'
    }

    error_list = []

    for idx, row in df_in.iterrows():
        customer = str(row[in_customer_col]).strip()

        if customer not in VALID_CUSTOMERS:
            error_list.append(
                f"第{idx + 2}行，客户='{customer}'"
            )

    if error_list:
        raise ValueError(
            "来货明细客户填写有误：\n" +
            "\n".join(error_list)
        )

    # ========= 初始化 =========
    df_po.insert(0, '序号', range(1, len(df_po) + 1))
    df_po['来货数量'] = 0

    # 按【客户+SKU】汇总来货
    arrival_dict = {}

    for _, row in df_in.iterrows():

        customer = str(row[in_customer_col]).strip()
        sku = str(row[in_sku_col]).strip()

        qty = row[in_qty_col]

        if pd.isna(qty):
            qty = 0

        key = (customer, sku)

        arrival_dict[key] = arrival_dict.get(key, 0) + qty

    remain_list = []

    # ========= 分配 =========
    for (customer, sku), total_arrival_qty in arrival_dict.items():

        remain_qty = total_arrival_qty

        mask = (
            (df_po[po_customer_col].astype(str).str.strip() == customer)
            &
            (df_po[po_sku_col].astype(str).str.strip() == sku)
        )

        po_rows = (
            df_po[mask]
            .sort_values('源单单号')
        )

        for idx, po_row in po_rows.iterrows():

            if remain_qty <= 0:
                break

            po_qty = po_row[po_qty_col]

            current_allocated = df_po.at[idx, '来货数量']

            available_qty = po_qty - current_allocated

            if available_qty <= 0:
                continue

            allocate_qty = min(remain_qty, available_qty)

            df_po.at[idx, '来货数量'] = (
                current_allocated + allocate_qty
            )

            remain_qty -= allocate_qty

        # 有剩余则输出补PR
        if remain_qty > 0:
            remain_list.append({
                '客户': customer,
                'sku': sku,
                '剩余数量': remain_qty
            })

    # ========= 导出 =========
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:

        df_in.to_excel(
            writer,
            sheet_name='来货数量',
            index=False
        )

        df_po.to_excel(
            writer,
            sheet_name='PO数量',
            index=False
        )

        if remain_list:
            df_remain = pd.DataFrame(remain_list)
        else:
            df_remain = pd.DataFrame(
                columns=['客户', 'sku', '剩余数量']
            )

        df_remain.to_excel(
            writer,
            sheet_name='补PR-SKU清单',
            index=False
        )

    output.seek(0)
    return output