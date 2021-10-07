import json, sqlite3, pandas as pd,pprint, numpy as np

def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('Key', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)




def load_dict(dict_file):
    with open(dict_file,'r') as f:
        return json.load(f)



def show_diff(df_key,df_stud,ordered=0,drop_same=True):

    df = df_key
    df2 = df_stud
    # Test if cols match
    # If extra coll - rename
    col_test(df,df2)
    col_match = True
    if col_match:
        df_all = pd.concat([df.reset_index(), df2.reset_index()],axis='columns', keys=['Key', 'Student'])
        df_final = df_all.swaplevel(axis='columns')[df.columns[0:]]
        if drop_same:
            #df_final = drop_non_diff_rows(df_final)
            drop_non_diff_rows(df_final)
            #df_final = df_final.drop_duplicates(subset=['Key','Student'],keep=False)
            #df_final = df_final[all(col[1] != col.'Student' for col in df_final.columns.values)]
    df_final = df_final.style.apply(highlight_diff, axis=None)
    return df_final



def drop_non_diff_rows(df):
    cols = df.columns
    to_drop = []
    for i, row in df.iterrows():
        #print(i)
        flag = 1
        for j in range(0,len(df.columns),2):
            if row[cols[j]] != row[cols[j+1]]:
                flag = 0
        if flag:
            to_drop.append(i)
    df.drop(to_drop,inplace=True)




def show_diff_all(student_dict,answer_dict,drop_same=True):
    for ccid in student_dict:
        show_diff_one(ccid,student_dict,answer_dict,drop_same=drop_same)



def show_diff_one(ccid,student_dict,answer_dict,drop_same=True,check_points=True):
    #give option for all students, or one student
    for q_num in student_dict[ccid]['dfs']:

        print('/'*8 + '~'*16 + f'{ccid}-{q_num}' + '~'*16 + '\\'*8 )
        if check_points:
            if student_dict[ccid]['points'][q_num].split('/')[0] == student_dict[ccid]['points'][q_num].split('/')[1] :
                print('The student has been awarded the points,\nso the dataframes are equal')
                continue
        df_stud = pd.read_json(student_dict[ccid]['dfs'][q_num])
        df_key = pd.read_json(answer_dict[q_num]['df'])

        display(show_diff(df_key,df_stud,drop_same=drop_same))



def matching_cols(key_df,stud_df):
    # Takes two dataframes and returns the most likley matches as a list of tuples
    # If there are more student cols then key cols, they will be alone in the tuple
    #otherwise it will be [(stud_col,key,col)...]
    key_cols = key_df.columns
    stud_cols = stud_df.columns
    extra_stud_cols = list(set(stud_cols)-set(key_cols))
    remaining_key_cols = list(set(key_cols)-set(stud_cols))
    for s_col in extra_stud_cols:
        stud_col_list = stud_df[s_col].tolist()
        res = (key_df.isin(stud_col_list).sum()/key_df.shape[0])*100

        print(s_col,res,type(res))


def col_test(key_df,stud_df):
    to_ret = []
    if len(key_df.columns) > len(stud_df.columns):
        print('Student is missing column(s)')
        missing_cols = list(set(key_df.columns) - set(stud_df.columns))
        #print(missing_cols)
        # add mising columns as null coulumns
        for col in missing_cols:
            stud_df[col] = ""
        to_ret = 0
    elif len(key_df.columns) < len(stud_df.columns):
        extra_cols = list(set(stud_df.columns) - set(key_df.columns))
        print('Student has an extra column(s)')
        #print(extra_cols)
        to_ret = stud_df[extra_cols]
        to_ret
    # The above might not be good / nessecary
    # Check for cols that dont match, matching cols will have same name as side effect from comparison earlier
    matched_cols = []
    for k_col in key_df.columns:
        for s_col in stud_df.columns:
            if k_col in matched_cols:
                break
            if s_col == k_col:
                matched_cols.append(k_col)
                break