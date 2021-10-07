'''
Diff like script for comparing SQL
Idea:
Key in JSON
student question in JSON / inputed

Either outputs match
or
If col names match
    Higlight nonmatching rows/cols
    Percent missing?

'''
import json, sqlite3, pandas as pd,pprint, os,re,csv,datetime as dt, numpy as np, tarfile

DB_FILE = r'C:\Users\Gerun\PycharmProjects\291Internship\script_grader\MA3small.db'
ANS_PATH = r"C:\Users\Gerun\PycharmProjects\291Internship\script_grader\downloaded_answers"
def main():

    #TODO - Add flags (?)
    print('hello')
    answer_dict = {}
    student_dict = {}
    load_student_answers(ANS_PATH,student_dict,answer_dict,DB_FILE)
    pprint.pprint(student_dict)
    while(True):
        # Make terminal like interface
        db_file = input('Enter the database file or path to the database file: ')
        print('Enter 0 for help with the intended workflow')
        print('Enter 1 to input an answer key')
        print('Enter 2 to load an answer key from file')
        print('Enter 3 to run the answer queries to be compared')
        print('Enter 4 to load student answers from a file')
        print('Enter 5 to run the student answers to be compared')
        print('Enter 6 to compare the key and student answers')
        print('Enter 7 to see the diff for students')
        #TODO - Move this all to be ran on jupyter
        print('Enter 8 to export student grades to a csv ')
        print('Enter e to exit')

        x = input('Input:')
        if 'e' in x.lower():
            break
        x = int(x)
        if x == 0:
            pass
        elif x == 1:
            create_key()
        elif x == 2:
            key_file = input('Enter the name of the .json file to load from')
            answer_dict = load_key_answers_json(key_file)
        elif x == 3:
            key_file = input('Enter the name of the .json file to load from')
            create_key_answers(key_file,db_file)
        elif x == 4:
            if answer_dict == {}:
                print('load an answer dict to continue')
                continue
            stud_dir = input('Enter the directory with the students answers')
            load_student_answers(stud_dir,student_dict,answer_dict,db_file)
        elif x == 5:
            if answer_dict == {}:
                print('load a student dict to continue')
                continue
            create_student_answers(student_dict,db_file)
        elif x == 6:
            if answer_dict == {}:
                print('load an answer dict to continue')
                continue
            if student_dict == {}:
                print('load a student dict to continue')
                continue
            compare_student_answers(student_dict,answer_dict)
        elif x == 7:
            pass
        elif x == 8:
            file_name = input('Enter the file name or file path')
            export_grades_to_csv(student_dict,answer_dict,file_name)

    #create_key()
    #create_key_answers('a.json',DB_FILE)
    ans_dict = load_key_answers_json('a_answers.json')
    student_dict = {}
    load_student_answers(r'C:\Users\Gerun\PycharmProjects\291Internship\script_grader\student_answers\A1',student_dict,ans_dict,DB_FILE)
    pprint.pprint(student_dict)
    compare_student_answers(student_dict,ans_dict)
    pprint.pprint(student_dict)
    pprint.pprint(ans_dict)
    export_grades_to_csv(student_dict,ans_dict,'grades')
    #parse_answers_txt(r'C:\Users\Gerun\PycharmProjects\291Internship\script_grader\student_answers\A1\0001_answers.txt',{})
    #view_key_answers('y_answers.json')
    #create_key()
    #create_answers('z.json',r'C:\Users\Gerun\PycharmProjects\291Internship\MAs\streaming.db')

def create_key():
    '''
    Creates the key query .txt file (queries in plain text)
    :return: nothing
    '''
    title = input('Enter name of key (eg. streaming_group_key): ')

    data = {}
    while(True):
        q_code = input('Enter the question number (eg. q1)\nor enter "e" to exit: ')
        if q_code == 'e':
            break
        ans = multiline_input('Copy the answer from the key,\nshould be on multiple lines: ')
        data[q_code] =  {}
        data[q_code]['answer'] = ans.replace('\n',' ')
        pts = input('Enter how many points the question is worth: ')
        data[q_code]['points'] = int(pts)
        if 'order by' in ans:
            data[q_code]['ordered'] = 1
        else:
            data[q_code]['ordered'] = 0
    pprint.pprint(data)
    with open(f'{title}.json','w',encoding='utf-8') as f:
        json.dump(data,f, ensure_ascii=False, indent=4)


def multiline_input(x):
    '''
    Handles copy - pasted multiline strings
    :param x: The multiline string to handle
    :return:
    '''
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)

def create_key_answers(key_file,db_file):
    '''
    Creates the answers for the key in the form of JSON serialized
    pandas dataframes, in a .json file
    The json file is made in the same directory as the key answer .txt file
     with _answers appended on the file nae
    :param key_file: The .txt file with the key queries
    :param db_file: The SQLite database file to connect to
    :return:nothing
    '''
    conn = sqlite3.connect(db_file)
    with open(key_file,'r') as f:
        queries = json.load(f)
        answers = {}
        for q_num in queries:
            answers[q_num] = {}
            query = queries[q_num]['answer']
            df = pd.read_sql_query(query, conn)
            answers[q_num]['df'] = df.to_json()
            answers[q_num]['points'] = queries[q_num]['points']
            answers[q_num]['ordered'] = queries[q_num]['ordered']
        newFile = key_file.split('.')[0] + '_answers.json'
        with open(newFile,'w',encoding='utf-8') as f:
            json.dump(answers,f, ensure_ascii=False, indent=4)


def load_key_answers_json(key_file):
    '''
    Providies an alternative to typing in the key answers, or can use an already made key - file
    :param key_file: The .txt file with the key queries
    :return: The answer dictionary
    '''
    # Loads answers from JSOn to a dict, returns said dict
    with open(key_file) as json_file:
        return json.load(json_file)

def create_student_answers(student_dict,db_file):
    '''
    Creates the answers for the students in the form of JSON serialized
    pandas dataframes, in a .json file
    :param student_dict: The dictionary with student information
    :param dbFile: The SQLite database file to connect to
    :return:nothing
    '''
    conn = sqlite3.connect(db_file)
    for ccid in student_dict:
        student_dict[ccid]['dfs'] = {}
        for q_num in student_dict[ccid]['queries']:
            print(q_num)
            query = student_dict[ccid]['queries'][q_num]
            print(query)

            try:
                df = pd.read_sql_query(query, conn)
                student_dict[ccid]['dfs'][q_num] = df.to_json()
            except pd.io.sql.DatabaseError:
                print(f'Error creating dataframe on {ccid} - {q_num}')
                student_dict[ccid]['dfs'][q_num] = pd.DataFrame().to_json()

def compare_student_answers(student_dict,ans_dict):
    '''
    Compares the student answers with the answer key, assigns grades to the student_dict
    also makes a file containing the student dictionar information
    :param student_dict: The dictionary with student information
    :param ans_dict: The dictionary with answer information
    :return:nothing
    '''
    for ccid in student_dict:
        student_dict[ccid]['points'] = {}
        for q_num in student_dict[ccid]['dfs']:
            print(f'{ccid}-{q_num}')
            pts = ans_dict[q_num]['points']
            try:
                df_stud = pd.read_json(student_dict[ccid]['dfs'][q_num])
            except:
                df_stud = pd.DataFrame()
            df_key = pd.read_json(ans_dict[q_num]['df'])

            if compare_df(df_key,df_stud,ans_dict[q_num]['ordered']):
                student_dict[ccid]['points'][q_num] = f'{pts}/{pts}'
            else:
                student_dict[ccid]['points'][q_num] = f'0/{pts}'

    with open(f'student_dict-{str(dt.datetime.now()).split(" ")[0]}.json','w',encoding='utf-8') as f:
        json.dump(student_dict,f, ensure_ascii=False, indent=4)
def load_student_answers(ans_path,stud_dict,ans_dict,db_file):
    '''
    Loads the student answers from the directory containing the student answer files
    :param ans_path: The path with the student answer files
    :param stud_dict: The dictionary with student information
    :param ans_dict: The dictionary with answer information
    :param db_file: the SQLite database file to connect to
    :return: nothing
    '''
    untar(ans_path)
    with os.scandir(ans_path) as ans_dir:
        for entry in ans_dir:

            query_paths = []
            ccid = ''
            for stud_file in os.scandir(entry.path):

                if stud_file.name.endswith(".tgz") and stud_file.is_file():
                    ccid = stud_file.name.split('-')[0]
                    build_dict(ccid,stud_dict)
                if re.match('^[0-9]+.sql',stud_file.name):
                    query_paths.append(stud_file)
            update_student_answers_json(ccid,query_paths,stud_dict,ans_dict,db_file)

def build_dict(ccid,stud_dict):
    if ccid not in stud_dict:
        stud_dict[ccid] = {}
        stud_dict[ccid]['queries'] = {}

def update_student_answers_json(ccid,stud_query_paths,stud_dict,key_json,db_file):

    parse_answers_txt(ccid,stud_query_paths,stud_dict)
    # At this point 0 stud_dict is updated with student answers in text

    # Get student answers in df form
    create_student_answers(stud_dict,db_file)
    #if compare_df(ans_dict)

def parse_answers_txt(ccid,file_paths,stud_dict):
    '''
    Parsese the student answers from the .txt file into
    :param file_path: the file path containing the student answers
    :param stud_dict: The dictionary with student information
    :return: nothing
    '''
    for file_path in file_paths:
        with open(file_path.path,'r') as f:
            query_start = False

            query = []
            for row in f:
                #print(row)
                if query_start:
                    query.append(row.strip('\n'))

                elif not query_start and row.strip().split(' ',1)[0].lower() == "select":
                    query.append(row.strip('\n'))
                    query_start = True
            #print(' '.join(query),type(' '.join(query)))

                    ##
            stud_dict[ccid]['queries'][file_path.name.split('.')[0]] = ' '.join(query)
    pprint.pprint(stud_dict)


def export_grades_to_csv(student_dict,answer_dict,file_name):
    '''
    exports grades to csv
    :param student_dict: The dictionary with student information
    :param answer_dict: The dictionary with answer information
    :param file_name: The file name to write to, should not have the .csv
    :return: nothing
    '''

    rows = []
    q_nums = []
    total = 0
    for question in answer_dict:
        q_nums.append(question)
        total += int(answer_dict[question]['points'])
    q_nums.sort()
    for ccid in student_dict:
        row = {'ccid':ccid}
        stud_pts = 0
        for q_num in student_dict[ccid]['points']:
            row[q_num] = student_dict[ccid]['points'][q_num].split('/')[0]
            stud_pts += int(student_dict[ccid]['points'][q_num].split('/')[0])
        row['stud_pts'] = stud_pts
        rows.append(row)

    #Make header
    header = ['ccid']
    for q_num in q_nums:
        header.append(q_num)
    header.append('overall (points)')
    header.append('overall (%)')
    #Make final rows
    final_rows = [header]
    for row in rows:
        final_row = [row['ccid']]
        for q_num in q_nums:
            if q_num not in row:
                final_row.append(0)
            else:
                final_row.append(row[q_num])
        final_row.append(row['stud_pts'])
        final_row.append((int(row['stud_pts'])/total)*100)
        final_rows.append(final_row)
    with open(f'{file_name}.csv','w', newline='') as f:
        csv.writer(f, delimiter=',',
                   quotechar='|', quoting=csv.QUOTE_MINIMAL).writerows(final_rows)





def compare_df(corr_res,stud_result,ordered):
    '''
    Compares the student answer df with the key anwser df
    :param corr_res: the correct result df
    :param stud_result: the student result df
    :param ordered: if the query is ordered or not
    :return:
    '''
    if corr_res.equals(stud_result):
        return 1
    if not ordered:
        print('--------------------------------------------SORTING-----------------------------------')
        corr_res = corr_res.sort_values(by=corr_res.columns.to_list()).reset_index(drop=True)
        # If cant sort student result by the collumns of teh correct result, then does not have right cols
        try:
            stud_result = stud_result.sort_values(by=corr_res.columns.to_list()).reset_index(drop=True)
        except KeyError as ke:
            print('_______________________________________KEY ERROR___________________________________')
    #TRY RENAMING LIKE COLS
    for corr_col in corr_res.columns:
        #print(corr_col,type(corr_col))
        for stud_col in stud_result.columns:
            if corr_col != stud_col and corr_res[corr_col].equals(stud_result[stud_col]):
                print('____REACHED___')
                stud_result.rename(inplace=True,columns={stud_col:corr_col})


    # Then compare dfs, ignoring column order
    try:
        print('reached check_like')
        pd.testing.assert_frame_equal(corr_res,stud_result,check_like=True,check_names=False)
        return 1
    except AssertionError as ae:
        return 0
    return 0

def key_stud_diff():
    '''
    Shows the diff between key and student
    Cases:
        Columns line up
            - Show different rows
        Columns dont line up
            - If names different, show columns that are equal with different names
                - on the key / student version

            - If num different
                - Use pandas matching to find coulms without a matching name or data values
                - If
    :return:
    '''

    pass
def view_key_answers(key_answer_file):
    '''
    view key answers
    :param key_answer_file:
    :return:
    '''
    with open(key_answer_file,'r') as f:
        results = json.load(f)

        for code in results:
            print(code)
            print(pd.read_json(results[code]))

def load_key():
    pass

def untar(path):

    for path, directories, files in os.walk(path):
        for f in files:
            if f.endswith(".tgz"):
                tar = tarfile.open(os.path.join(path,f), 'r:gz')
                tar.extractall(path=path)
                tar.close()

# ---------------JUPYTER FUNCTIONS--------------------
def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('Key', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)




def drop_non_diff_rows(df):
    pass
    for col in df.columns.values:
        print(col,type(col))



def show_diff(df_key,df_stud,ordered=0,drop_same=True):

    df = df_key
    df2 = df_stud
    # Test if cols match
    # If extra coll - rename
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




main()


