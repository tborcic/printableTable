class printableTable:
	def __init__(self):
		self.style_default()
		self.table = []
		self.tableWidth = {}
		self.middleAllign = []
		self.rightAllign = []
		self.titles = [0]
		self.totalWidth = 0
		self.spacing = 2

	def setTo(self, obj):
		if(obj.style=='default'):
			self.style_default()
		elif(obj.style=='new'):
			self.style_differentColumns()
		elif(obj.style=='noSeperator'):
			self.style_noSeperators()
		self.table = obj.table.copy()
		self.tableWidth = obj.tableWidth.copy()
		self.middleAllign = obj.middleAllign.copy()
		self.rightAllign = obj.rightAllign.copy()
		self.titles = obj.titles.copy()
		self.totalWidth = obj.totalWidth

	def style_default(self):
		self.style = 'default'
		self.cornerTop = '.'
		self.cornerBottom = '\''
		self.rowSeperator = '-'
		self.rowSeperator2 = '·'
		self.rowSeperatorEdge = ':'
		self.columnSeperator = '|'
		self.columnSeperator2 = '|'
		self.columnSeperatorMiddle = '+'
		self.drawTitleSeperator = True
		self.drawRowSeperators = True

	def style_differentColumns(self):
		self.style = 'new'
		self.cornerTop = '.'
		self.cornerBottom = '\''
		self.rowSeperator = '-'
		self.rowSeperator2 = '-'
		self.rowSeperatorEdge = '+'
		self.columnSeperator = '|'
		self.columnSeperator2 = ':'
		self.columnSeperatorMiddle = '+'
		self.drawTitleSeperator = True
		self.drawRowSeperators = False

	def style_noSeperators(self):
		self.style = 'noSeperator'
		self.cornerTop = ' '
		self.cornerBottom = ' '
		self.rowSeperator = ' '
		self.rowSeperator2 = ' '
		self.rowSeperatorEdge = ' '
		self.columnSeperator = ' '
		self.columnSeperator2 = ' '
		self.columnSeperatorMiddle = ' '
		self.drawTitleSeperator = True
		self.drawRowSeperators = False
	
	def clear(self):
		self.table.clear()
		self.tableWidth.clear()
		self.middleAllign.clear()
		self.rightAllign.clear()
		self.extraTitle = False
		self.titles.clear()
		self.titles.append(0)
		self.totalWidth = 0

	def getTotalWidth(self):
		totalWidth = 0
		for _,row in self.tableWidth.items():
			tempLen = 0
			for item in row:
				tempLen+= item + self.spacing
			if(tempLen>totalWidth):
				totalWidth=tempLen
		return totalWidth


	def getArrayTotalLength(self,arr):
		output = 0
		for item in arr:
			output+= item + self.spacing
		return output

	def setTableWidth(self):
		# make an dictionary containing number of elements and an 
		# array of max width for that number of elements
		widthArray = {}
		for row in self.table:
			if(type(row) is str):
				row = [row]
			if (len(row) in widthArray.keys()):
				for index,item in enumerate(row):
					itemLen = len(str(item))
					if(isinstance(item, list)):
						itemLen-=2 #[] at begining and end of list conversion to string
					if (itemLen > widthArray[len(row)][index]):
						widthArray[len(row)][index] = itemLen
			else:
				widthArray[len(row)] = []
				for item in row:
					itemLen = len(str(item))
					widthArray[len(row)].append(itemLen)
		self.tableWidth = widthArray
		
		#sets the width of the table
		self.totalWidth = self.getTotalWidth()

		#expands the tableWidth array so that each element expands
		#till it has the same width as the table
		maxElements,_ = self.getMaxElements()
		for rowNum,row in widthArray.items():
			arrLen = self.getArrayTotalLength(row)
			arrDif = self.totalWidth - arrLen + maxElements - rowNum
			
			if(arrDif > 0):
				remanining = arrDif
				while (remanining>0):
					for i in range(0,rowNum):
						if(remanining==0):
							break
						self.tableWidth[rowNum][i] += 1
						remanining-=1

	def setTitles(self,arr):
		self.titles.clear()
		for i in arr:
			self.titles.append(i)

	def getMaxElements(self):
		maxElem = 0
		maxElemIndex = 0
		for index,row in enumerate(self.table):
			if (type(row) is str):
				row =[row]
			itemCount = len(row)
			if (itemCount>maxElem):
				maxElem = itemCount
				maxElemIndex = index
		return maxElem,maxElemIndex
	
	def addSeperation(self, rowNumber):
		for index,string in enumerate(self.table[rowNumber]):
			output = ''
			for s in string:
				output += s + ' '
			output = output[:-1]
			self.table[rowNumber][index]=output

	def addSeperationStr(self, item):
		output = ''
		for i in item:
			output += i + ' '
		return output[:-1]

	def addRow(self, arr):
		self.table.append(arr)

	def getRowSeperatorFormat(self, item, rowSeperator, length, columnSeperator):
		return '{:{}<{}}{}'.format(item,rowSeperator, length, columnSeperator)

	def getRowSeperator(self, edgeChar, rowSeperator, columnSeperator, seperationLen=0):
		output = edgeChar
		if (seperationLen > 0):
			output += self.getRowSeperatorFormat('',rowSeperator, seperationLen, columnSeperator)
		else:
			tableLen,_ = self.getMaxElements()
			for _ in range(0,tableLen):
				output += self.getRowSeperatorFormat('',rowSeperator, self.getTotalWidth(), columnSeperator)
			output = output[:-1]
		output += edgeChar +'\n'
		return output

	def getRowFormat(self, item, length, columnSeperator, allignmMent):
		if (allignmMent == 'middle'):
			return ' {:^{}s} {}'.format(item, length, columnSeperator)
		elif (allignmMent == 'right'):
			return ' {:>{}s} {}'.format(item, length, columnSeperator)
		elif (allignmMent == 'left'):
			return ' {:<{}s} {}'.format(item, length, columnSeperator)

	def getRow(self,arr, seperator, columnSeperator, seperateRow, allignmMent = 'left'):
		output = columnSeperator
		for column in range(0,len(arr)):
			if (type(arr[column]) is list):
				columnModified = ''
				for item in arr[column]:
					columnModified += '{}, '.format(str(item))
				columnModified = columnModified[:-2]
			else:
				columnModified = str(arr[column])
			output += self.getRowFormat(columnModified,self.tableWidth[len(arr)][column], columnSeperator, allignmMent)
		output = output[:-1]
		output += columnSeperator +'\n'
		if(seperateRow):
			output += self.getRowSeperator(self.rowSeperatorEdge, seperator, self.columnSeperatorMiddle)
		return output
	
	def getTable(self):
		self.setTableWidth()
		maxElements,_ = self.getMaxElements()
		totalWidth = self.totalWidth + maxElements - 2
		output = self.getRowSeperator(self.cornerTop, self.rowSeperator, self.rowSeperator, seperationLen=totalWidth)
		for index,row in enumerate(self.table):
			if(type(row) is str):
				row = [row]
			allignmMent = 'left'
			if (index in self.middleAllign):
				allignmMent = 'middle'
			elif (index in self.rightAllign):
				allignmMent = 'right'
			output+=self.getRow(row,self.rowSeperator,self.columnSeperator, False ,allignmMent=allignmMent)
			if(index == 0 and self.drawTitleSeperator):
				output += self.getRowSeperator(self.rowSeperatorEdge, self.rowSeperator, self.rowSeperator,seperationLen=totalWidth)
			elif(self.drawRowSeperators):
				if(index != len(self.table)-1):
					output += self.getRowSeperator(self.rowSeperatorEdge, self.rowSeperator, self.rowSeperator,seperationLen=totalWidth)
			pass
		output  += self.getRowSeperator(self.cornerBottom, self.rowSeperator, self.rowSeperator,seperationLen=totalWidth)
		
		return output

	def getTableTitleFormat(self, title, allignmMent='middle'):
		self.setTableWidth()
		return self.getRowFormat(str(title), self.getTotalWidth()+3,'',allignmMent=allignmMent)

if __name__ == "__main__":
	arr = [ [1,	2,	3,	4 ],
			[5,	6,	7,	8 ],
			[10,11,	12,	13] ]

	arr2 = [[1,		2,	[3,3,3]	, 4 ],
			[5,		6,	7		, 8 ],
			[10,	11,	12		, 13] ]

	titlesArr = ['first','second','third','fourth']
	title = 'test'

	
	newTable = printableTable()
	newTable.addRow(title) 
	for row in arr:
		newTable.addRow(row)
	print(newTable.getTable())

	newTable.clear()
	newTable.addRow(titlesArr)
	for row in arr:
		newTable.addRow(row)
	print(newTable.getTable())

	newTable.clear()
	newTable.addRow(titlesArr) 
	for row in arr2:
		newTable.addRow(row)
	print(newTable.getTable())

	newTable.clear()
	newTable.addRow(title) 
	newTable.addRow(titlesArr)
	for row in arr:
		newTable.addRow(row)
	print(newTable.getTable())

	#print('1 title, 10 items')
	newTable.clear()
	newTable.addRow('test')
	newTable.addRow(['t','e','s','t','s','t','e','s','t','s'])
	print(newTable.getTable())

	newTable.clear()
	newTable.addRow('test') 
	newTable.addRow(['t'])
	print(newTable.getTable())

	newTable.clear()
	newTable.style_differentColumns()
	newTable.addRow(title) 
	newTable.addRow(titlesArr)
	for row in arr:
		newTable.addRow(row)
	print(newTable.getTable())

	newTable.clear()
	newTable.style_noSeperators()
	newTable.addRow(title) 
	newTable.addRow(titlesArr)
	for row in arr:
		newTable.addRow(row)
	newTable.middleAllign.append(0)
	print(newTable.getTable())

	newTable.clear()
	newTable.style_differentColumns()
	newTable.addRow(titlesArr)
	for row in arr:
		newTable.addRow(row)
	print(newTable.getTableTitleFormat('te|st'))
	print(newTable.getTable())

	newTable.clear()
	newTable.style_differentColumns()
	newTable.addRow([   1,      2   ])
	newTable.addRow([ 3,  4,  5,  6 ])
	newTable.addRow([1,2,3,4,5,6,7,8])
	newTable.middleAllign.append(0)
	newTable.middleAllign.append(1)
	newTable.middleAllign.append(2)
	print(newTable.getTableTitleFormat(1))
	print(newTable.getTable())

	newTable.clear()
	newTable.addRow([1,2,3,4,5,6])
	newTable.drawTitleSeperator = False
	print(newTable.getTableTitleFormat('random list'))
	print(newTable.getTable())
	
	newTable.clear()
	for i in range(0,10):
		arr = []
		for j in range(0,i+1):
			arr.append(j)
		newTable.addRow(arr)
		newTable.middleAllign.append(i)
	print(newTable.getTableTitleFormat('random list2'))
	print(newTable.getTable())