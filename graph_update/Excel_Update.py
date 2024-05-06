import openpyxl
from openpyxl.drawing.image import Image

# Excelファイルをロード
wb = openpyxl.load_workbook('/Users/ooekenfutoshi/Desktop/資産推移.xlsx')
ws = wb.active

# 最後のグラフを見つける
graphs = [obj for obj in ws._images if isinstance(obj, Image)]
if graphs:
    last_graph = graphs[-1]  # 最新のグラフを取得

    # グラフの位置を取得し、2行下に設定
    new_row = last_graph.anchor._from.row + 24  # 2行下に移動
    new_col = last_graph.anchor._from.col

    # 新しい位置にグラフをコピー
    new_graph = Image(last_graph.path)
    ws.add_image(new_graph, anchor=ws.cell(row=new_row, column=new_col).coordinate)

    # ファイルを保存
    wb.save('modified_example.xlsx')
else:
    print("グラフが見つかりませんでした。")



