list1 = [1,1,1,2,2,2,3,3,3]


uniques = []

for l in list1:
    if l  not in uniques:
        uniques.append(l)
# print(uniques)

counts = []
for u in uniques:
    c=0 # uniques = [1,2,3]
    for l in list1: # list1 = [1,2,2,3,3]
        if u ==l:
            c+=1
    counts.append(c)

#counts=[1,2,2]
# find max freq in counts
max_freq = counts[0]
for c in counts:
    if c > max_freq:
        max_freq = c

res = []
for u,c in zip(uniques, counts):
    if max_freq == c:
        res.append(u)
print(res)


