import xlwt
book=xlwt.Workbook(encoding='utf-8',style_compression=0)#创excel
sheet=book.add_sheet('test',cell_overwrite_ok=True)#创sheet
sheet.write(0,0,'EnglishName')#写入
sheet.write(1,0,'Marcovaldo')
txt1='中文名'
txt2='马瓦卡多'
sheet.write(0,1,txt1)
sheet.write(1,1,txt2)#不用decode，直接写str就可以
book.save(r'excelTest.xls')#存储