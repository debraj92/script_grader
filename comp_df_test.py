import json, sqlite3, pandas as pd,pprint, numpy as np
from sql_diff import compare_df
from collections import OrderedDict as od
DB = 'streaming.db'
def test():
    print('Same all: expect 1')
    q1_key = "{\"year\":{\"0\":2012,\"1\":2018,\"2\":2017,\"3\":2016,\"4\":2010,\"5\":2009,\"6\":2020,\"7\":2015,\"8\":2014,\"9\":2011,\"10\":2019,\"11\":2008,\"12\":2007,\"13\":2006,\"14\":2003,\"15\":1996,\"16\":1989,\"17\":1988},\"count()\":{\"0\":6,\"1\":5,\"2\":3,\"3\":3,\"4\":3,\"5\":3,\"6\":2,\"7\":2,\"8\":2,\"9\":2,\"10\":1,\"11\":1,\"12\":1,\"13\":1,\"14\":1,\"15\":1,\"16\":1,\"17\":1}}"
    q1_student = "{\"year\":{\"0\":2012,\"1\":2018,\"2\":2017,\"3\":2016,\"4\":2010,\"5\":2009,\"6\":2020,\"7\":2015,\"8\":2014,\"9\":2011,\"10\":2019,\"11\":2008,\"12\":2007,\"13\":2006,\"14\":2003,\"15\":1996,\"16\":1989,\"17\":1988},\"count()\":{\"0\":6,\"1\":5,\"2\":3,\"3\":3,\"4\":3,\"5\":3,\"6\":2,\"7\":2,\"8\":2,\"9\":2,\"10\":1,\"11\":1,\"12\":1,\"13\":1,\"14\":1,\"15\":1,\"16\":1,\"17\":1}}"
    df_key = pd.read_json(q1_key)
    df_stud = pd.read_json(q1_student)
    print(compare_df(df_key,df_stud,0))

    #NOTE: CANT FIGURE OUT INDEX NAMES
        # PROBABLY DISREGARD I THINK I GOT IT
    print('Same values different column name: expect 1')
    q1_key = "{\"language\":{\"0\":\"English\",\"1\":\"German\"},\"AVG(n.runtime)\":{\"0\":92.1641659312,\"1\":107.0683760684}}"
    q1_student = "{\"language\":{\"0\":\"English\",\"1\":\"German\"},\"AVG(netflix.runtime)\":{\"0\":92.1641659312,\"1\":107.0683760684}}"
    df_key = pd.read_json(q1_key)
    df_stud = pd.read_json(q1_student)
    print(compare_df(df_key,df_stud,0))

    print('Same col name different values: expect 0')
    q1_key = "{\"language\":{\"0\":\"English\",\"1\":\"German\"},\"AVG(n.runtime)\":{\"0\":92.0,\"1\":107.0683760684}}"
    q1_student = "{\"language\":{\"0\":\"English\",\"1\":\"German\"},\"AVG(n.runtime)\":{\"0\":92.1641659312,\"1\":107.0683760684}}"
    df_key = pd.read_json(q1_key)
    df_stud = pd.read_json(q1_student)
    print(compare_df(df_key,df_stud,0))

    print('Same all different col order: expect 1')
    q1_key = "{\"language\":{\"0\":\"English\",\"1\":\"German\"},\"AVG(n.runtime)\":{\"0\":92.1641659312,\"1\":107.0683760684}}"
    q1_student = "{\"AVG(n.runtime)\":{\"0\":92.1641659312,\"1\":107.0683760684},\"language\":{\"0\":\"English\",\"1\":\"German\"}}"
    df_key = pd.read_json(q1_key)
    df_stud = pd.read_json(q1_student)
    #print(df_key,'\n',df_stud)
    print(compare_df(df_key,df_stud,0))

    print('Same all different row order: expect 1')
    q1_key = "{\"language\":{\"0\":\"English\",\"1\":\"German\"},\"AVG(n.runtime)\":{\"0\":92.0,\"1\":107.0683760684}}"
    q1_student = "{\"language\":{\"0\":\"German\",\"1\":\"English\"},\"AVG(n.runtime)\":{\"0\":107.0683760684,\"1\":92.0}}"
    df_key = pd.read_json(q1_key)
    df_stud = pd.read_json(q1_student)
    #print(df_key,'\n',df_stud)
    print(compare_df(df_key,df_stud,0))

    print('Changed data, showing diff func')
    q1_key = "{\"year\":{\"0\":2012,\"1\":2018,\"2\":2017,\"3\":2016,\"4\":2010,\"5\":2009,\"6\":2020,\"7\":2015,\"8\":2014,\"9\":2011,\"10\":2019,\"11\":2008,\"12\":2007,\"13\":2006,\"14\":2003,\"15\":1996,\"16\":1989,\"17\":1988},\"count()\":{\"0\":6,\"1\":5,\"2\":3,\"3\":3,\"4\":3,\"5\":3,\"6\":2,\"7\":2,\"8\":2,\"9\":2,\"10\":1,\"11\":1,\"12\":1,\"13\":1,\"14\":1,\"15\":1,\"16\":1,\"17\":1}}"
    q1_student = "{\"year\":{\"0\":2012,\"1\":2018,\"2\":2017,\"3\":2016,\"4\":2010,\"5\":2009,\"6\":2020,\"7\":2015,\"8\":2014,\"9\":2011,\"10\":2019,\"11\":2008,\"12\":2007,\"13\":2006,\"14\":2003,\"15\":1996,\"16\":1989,\"17\":1988},\"count()\":{\"0\":7,\"1\":6,\"2\":3,\"3\":3,\"4\":3,\"5\":3,\"6\":2,\"7\":2,\"8\":2,\"10\":2,\"10\":1,\"11\":1,\"12\":1,\"13\":1,\"14\":1,\"15\":1,\"16\":4,\"17\":1}}"
    df = pd.read_json(q1_key)
    df2 = pd.read_json(q1_student)
    print(compare_df(df_key,df_stud,0))

    df_all = pd.concat([df.set_index('year'), df2.set_index('year')],axis='columns', keys=['First', 'Second'])
    print(df_all)
    df_final = df_all.swaplevel(axis='columns')[df.columns[1:]]
    df_final.style.apply(highlight_diff, axis=None)
    print(df_final.style.apply(highlight_diff, axis=None))


def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('First', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)


'''You can use this function, the output is an ordered dict of 6 dataframes which you can write to excel for further analysis.

'df1' and 'df2' refers to your input dataframes.
'uid' refers to the column or combination of columns that make up the unique key. (i.e. 'Fruits')
'dedupe' (default=True) drops duplicates in df1 and df2. (refer to Step 4 in comments)
'labels' (default = ('df1','df2')) allows you to name the input dataframes. If a unique key exists in both dataframes, but have different values in one or more columns, it is usually important to know these rows, put them one on top of the other and label the row with the name so we know to which dataframe does it belong to.
'drop' can take a list of columns to be excluded from the consideration when considering the difference
Here goes:

df1 = pd.DataFrame([['apple', '1'], ['banana', 2], ['coconut',3]], columns=['Fruits','Quantity'])
df2 = pd.DataFrame([['apple', '1'], ['banana', 3], ['durian',4]], columns=['Fruits','Quantity'])
dict1 = diff_func(df1, df2, 'Fruits')

In [10]: dict1['df1_only']:
Out[10]:
    Fruits Quantity
1  coconut        3

In [11]: dict1['df2_only']:
Out[11]:
   Fruits Quantity
3  durian        4

In [12]: dict1['Diff']:
Out[12]:
   Fruits Quantity df1 or df2
0  banana        2        df1
1  banana        3        df2

In [13]: dict1['Merge']:
Out[13]:
  Fruits Quantity
0  apple        1'''


def diff_func(df1, df2, uid, dedupe=True, labels=('df1', 'df2'), drop=[]):
    dict_df = {labels[0]: df1, labels[1]: df2}
    col1 = df1.columns.values.tolist()
    col2 = df2.columns.values.tolist()

    # There could be columns known to be different, hence allow user to pass this as a list to be dropped.
    if drop:
        print ('Ignoring columns {} in comparison.'.format(', '.join(drop)))
        col1 = list(filter(lambda x: x not in drop, col1))
        col2 = list(filter(lambda x: x not in drop, col2))
        df1 = df1[col1]
        df2 = df2[col2]


    # Step 1 - Check if no. of columns are the same:
    len_lr = len(col1), len(col2)
    assert len_lr[0]==len_lr[1], \
        'Cannot compare frames with different number of columns: {}.'.format(len_lr)

    # Step 2a - Check if the set of column headers are the same
    #           (order doesnt matter)
    assert set(col1)==set(col2), \
        'Left column headers are different from right column headers.' \
        +'\n   Left orphans: {}'.format(list(set(col1)-set(col2))) \
        +'\n   Right orphans: {}'.format(list(set(col2)-set(col1)))

    # Step 2b - Check if the column headers are in the same order
    if col1 != col2:
        print ('[Note] Reordering right Dataframe...')
        df2 = df2[col1]

    # Step 3 - Check datatype are the same [Order is important]
    if set((df1.dtypes == df2.dtypes).tolist()) - {True}:
        print ('dtypes are not the same.')
        df_dtypes = pd.DataFrame({labels[0]:df1.dtypes,labels[1]:df2.dtypes,'Diff':(df1.dtypes == df2.dtypes)})
        df_dtypes = df_dtypes[df_dtypes['Diff']==False][[labels[0],labels[1],'Diff']]
        print (df_dtypes)
    else:
        print ('DataType check: Passed')

    # Step 4 - Check for duplicate rows
    if dedupe:
        for key, df in dict_df.items():
            if df.shape[0] != df.drop_duplicates().shape[0]:
                print(key + ': Duplicates exists, they will be dropped.')
                dict_df[key] = df.drop_duplicates()

    # Step 5 - Check for duplicate uids.
    if type(uid)==str or type(uid)==list:
        print ('Uniqueness check: {}'.format(uid))
        for key, df in dict_df.items():
            count_uid = df.shape[0]
            count_uid_unique = df[uid].drop_duplicates().shape[0]
            var = [0,1][count_uid_unique == df.shape[0]] #<-- Round off to the nearest integer if it is 100%
            pct = round(100*count_uid_unique/df.shape[0], var)
            print ('{}: {} out of {} are unique ({}%).'.format(key, count_uid_unique, count_uid, pct))

    # Checks complete, begin merge. '''Remenber to dedupe, provide labels for common_no_match'''
    dict_result = od()
    df_merge = pd.merge(df1, df2, on=col1, how='inner')
    if not df_merge.shape[0]:
        print ('Error: Merged DataFrame is empty.')
    else:
        dict_result[labels[0]] = df1
        dict_result[labels[1]] = df2
        dict_result['Merge'] = df_merge
        if type(uid)==str:
            uid = [uid]

        if type(uid)==list:
            df1_only = df1.append(df_merge).reset_index(drop=True)
            df1_only['Duplicated']=df1_only.duplicated(subset=uid, keep=False)  #keep=False, marks all duplicates as True
            df1_only = df1_only[df1_only['Duplicated']==False]
            df2_only = df2.append(df_merge).reset_index(drop=True)
            df2_only['Duplicated']=df2_only.duplicated(subset=uid, keep=False)
            df2_only = df2_only[df2_only['Duplicated']==False]

            label = labels[0]+' or '+labels[1]
            df_lc = df1_only.copy()
            df_lc[label] = labels[0]
            df_rc = df2_only.copy()
            df_rc[label] = labels[1]
            df_c = df_lc.append(df_rc).reset_index(drop=True)
            df_c['Duplicated'] = df_c.duplicated(subset=uid, keep=False)
            df_c1 = df_c[df_c['Duplicated']==True]
            df_c1 = df_c1.drop('Duplicated', axis=1)
            df_uc = df_c[df_c['Duplicated']==False]

            df_uc_left = df_uc[df_uc[label]==labels[0]]
            df_uc_right = df_uc[df_uc[label]==labels[1]]

            dict_result[labels[0]+'_only'] = df_uc_left.drop(['Duplicated', label], axis=1)
            dict_result[labels[1]+'_only'] = df_uc_right.drop(['Duplicated', label], axis=1)
            dict_result['Diff'] = df_c1.sort_values(uid).reset_index(drop=True)

    return dict_result


test()