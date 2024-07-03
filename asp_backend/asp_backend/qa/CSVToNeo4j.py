# # =================================
# # File : CSVToNeo4j.py
# # Description :
# # Author : ChenX
# # CREATE TIME : 2024/1/14 15:54
# # =================================
# import pandas as pd
# import os
# from py2neo import Graph
#
# folder_path = './excel-v2'
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
# # 列出文件夹中所有的xlsx文件
# excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
#
# # 读取每个Excel文件
# for file in excel_files:
#     if file == '大类描述' or file == '关系':
#         continue
#     file_path = os.path.join(folder_path, file)
#     data = pd.read_excel(file_path)
#     # 删除指定对象属性列
#     if file == '事件实体v2':
#         # 开始时间	结束时间	持续时间	报道时间	发生时间	描述	标题	死亡人数	受伤人数	编号	InstanceOf	纬度	经度
#     elif file == '人物关系v2':
#         data = data.drop('所属组织', axis=1)
#     elif file == '地点实体v2':
#         data = data.drop('所在国家', axis=1)
#         data = data.drop('实际控制者', axis=1)
#     elif file == '组织实体v2':
#         data = data.drop('领导人', axis=1)
#         data = data.drop('总部所在地', axis=1)
#     elif file == '装备实体v2':
#         # data = data.drop('ColumnName', axis=1)
#     for index, row in data.iterrows():
#         # 创建一个节点
#         if file == '事件实体v2':
#             query = f"CREATE (p:Person {{ {', '.join([f'{key}: \'{value}\'' for key, value in row.items()])} }})"
#             graph.run("CREATE (e:Event {开始时间: $开始时间 持续时间: $age})", 开始时间=row['开始时间'], age=row['age'])
#         elif file == '人物关系v2':
#             graph.run("CREATE (p:Person {name: $name, age: $age})", name=row['name'], age=row['age'])
#         elif file == '地点实体v2':
#             graph.run("CREATE (p:Person {name: $name, age: $age})", name=row['name'], age=row['age'])
#         elif file == '组织实体v2':
#             graph.run("CREATE (p:Person {name: $name, age: $age})", name=row['name'], age=row['age'])
#         elif file == '装备实体v2':
#             graph.run("CREATE (p:Person {name: $name, age: $age})", name=row['name'], age=row['age'])
#
#     # 在这里处理每个文件的数据
#     # 例如，你可以在这里将数据插入到Neo4j数据库中
