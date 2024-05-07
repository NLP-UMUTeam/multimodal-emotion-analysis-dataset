"""
Bootstrapping

Contains a lot of stuff that is reused continously in all the packages

@author José Antonio García-Díaz <joseantonio.garcia8@um.es>
@author Rafael Valencia-Garcia <valencia@um.es>
"""

# For reproductibility, we set a global seed that will be shared on tensorflow, numpy, etc...
seed = 1 


# Import OS to set the environment variables
import os


# Import libreries that can generate stochastic behaviour
import random
import numpy as np
import pandas as pd
import sqlite3


# Seed random generators
# @todo improve https://scikit-learn.org/stable/common_pitfalls.html#randomness
def set_random_seed (seed):
    os.environ['PYTHONHASHSEED'] = str (seed)
    random.seed (seed)
    np.random.seed (seed)

set_random_seed (seed)


# Configure pretty print options
np.set_printoptions (formatter = {'float_kind': '{:.5f}'.format})
pd.set_option ('display.float_format', lambda x: '%.3f' % x)


def dict_factory (cursor, row):
    """
    @link https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
    """
    d = {}
    for idx, col in enumerate (cursor.description):
        d[col[0]] = row[idx]
    return d
    
    
def get_annotations (path):
    """
    @var path
    
    @return cursor
    """


    # @var conn SQLITE Connection
    conn = sqlite3.connect (path)
    conn.row_factory = dict_factory
    
    
    # @var sql_query String
    sql_query = """
        SELECT 
            annotations.* 
            
        FROM 
            annotations 

        WHERE 
            id IN (SELECT MAX(id) FROM annotations GROUP BY YOUTUBE_KEY, SEGMENT_AUDIO ORDER BY created_at DESC) AND 
            EMOTION <> 'discard'
    
    """;
    
    
    # @var cursor
    cursor = conn.cursor ()
    cursor = conn.execute (sql_query)
    
    return cursor

