# Read in all bite/non-bite files as DataFrame objects
bites_dir = '/home/steve/dml/activity-recognition/data/raw/bites/'
non_bites_dir = '/home/steve/dml/activity-recognition/data/raw/non-bites/'
file_ext = '.txt'
q = []
# Switch between bites_dir and non_bites_dir
for i in range (1,14):
	filename = non_bites_dir + str(i) + file_ext
	df = pd.read_csv(filename, header = 0, index_col = 4, names = ['x','y','z','delta','elapsed','class'])
	del df['delta']
	del df['class']
	q.append(df)

# Automatically extracting bite windows from raw bite data (done manually for non-bites)
# Find the sets of instances that mark where bites occur
y=[]
c = 2
for x in q:
	u = pd.DataFrame(columns=list('xyz'))
	u.index.names=['elapsed']
	i = 0
	while i < len(x):
		if x.iloc[i].z < 6.5:
			if len(x) > (i + 20) and i > 20:
				window = x.iloc[(i-20):(i+20), 0:3]
				df = pd.DataFrame(window, columns=['x','y','z'])
				df.index.names = ['elapsed']
				u = u.append(df)
				i+=50
		i+=1
	y.append(u)
	output = "/home/steve/dml/activity-recognition/data/parse/bites/" + str(c) + "-parsed.txt"
	u.to_csv(output)
	c+=1