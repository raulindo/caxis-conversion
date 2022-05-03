# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:35:33 2022

@author: Raul
"""

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def check_trend(df, name_col_trend='trend'):
    ''' Essa função recebe um dataframe com os dados da amostra e avalia se os dados de trend variam entre 0-90 ou 270-360
    
    '''
    
    if len(df[(df[name_col_trend]>90) & (df[name_col_trend]<270)])>0:
        print('O Dataframe tinha %0.0f linhas com valores de trends NÃO variando entre 0-90 ou 270-360. Essas linhas foram removidas.' %(len(df[(df[name_col_trend]>90) & (df[name_col_trend]<270)])))
        df = df.drop(df[(df['trend']>90) & (df['trend']<270)].index, inplace=True) # Drop linhas com valores de trend "ruins"
    else:
        print('O Dataframe tem todos valores de trend variando 0-90 ou 270-360. Tudo ok!')
        
    return 

def upper_plunge_dir(df, name_col_plunge_direction='pdir'):
    ''' Essa função torna os campos do Sentido de Plunge em letra maiúscula.
    '''

    df[name_col_plunge_direction] = df[name_col_plunge_direction].str.upper() # Torna maiúscula
    
    return

def check_plunge(df, name_col_plunge='plunge'):
    ''' Essa função recebe um dataframe com os dados da amostra e avalia se os dados de plunge variam entre 0-90;
        Caso alguma linha tenha valor de plunge maior do que 90 ela será excluída. 
    
    '''
    
    if len(df[(df[name_col_plunge]>90)])>0:
        print('O Dataframe tinha %0.0f linhas com valores de plunge maior do que 90. Essas linhas foram removidas.' %(len(df[(df[name_col_trend]>90) & (df[name_col_trend]<270)])))
        df = df.drop(df[(df['trend']>90) & (df['trend']<270)].index, inplace=True) # Drop linhas com valores de trend "ruins"
    else:
        print('O Dataframe não tem valores plunge maior do que 90. Tudo ok!')
        
    return 

def convert_plunge(row):
    ''' Essa função serve para converter os dados originais de plunge. 
    O nome da coluna de plunge deve ser plunge; essa função deve ser usada como um apply
    df['plunge_corrigido'] = df.apply(convert_plunge, axis=1)
    
    '''
    # converter o plunge é simples:
    # se pdir for E ou W, o plunge convertido = pungle original
    # se pdir for N ou S, o plunge convertido = 90 - plunge original
    if ((row['pdir'] == 'E') or (row['pdir']== 'W')):
        val = row['plunge']
        
    elif ((row['pdir'] == 'N') or (row['pdir']== 'S')):
        val = 90-row['plunge']

    return val

def convert_trend(row):
    ''' Essa função serve para converter os dados originais de TREND (azimute). 
    O nome da coluna de trend deve ser trend; essa função deve ser usada como um apply
    df['trend_corrigido'] = df.apply(convert_trend, axis=1)
    
    '''
    if (row['pdir'] == 'E'):
        if (row['trend']>269):
            val = 630 - row['trend']
        elif (row['trend']<91):
            val = 270 - row['trend']
            
    elif (row['pdir'] == 'W'):
        if (row['trend']>269):
            val = 450 - row['trend']
        elif (row['trend']<91):
            val = 90 - row['trend']
            
    elif (row['pdir'] == 'S'):
        val = 360 - row['trend']
        
    elif (row['pdir'] == 'N'):
        if (row['trend']>269):
            val = 540 - row['trend']
        elif (row['trend']<91):
            val = 180 - row['trend']
    
    return val

def load_file(filename="sample_cd11a.csv", sep=';', convert=True):
    
    ''' Essa função carrega o arquivo de dados de uma amostra e retorna um dataframe já com os valores de trend e plunge corrigidos;
        Durante a importação, também checa se os valores de trend variam dentro do intervalo correto e se há plunge maior do que 90. 
    '''
    df = pd.read_csv(filename, sep=sep)
    # Remove valores de trend variando de 0-90 ou 270-360
    check_trend(df)
    # Torna Campo de sentido de plunge em letras maiúsculas
    upper_plunge_dir(df)
    # Checa se tem plunge maior do que 90
    check_plunge(df)
    
    if convert:
        # convert trend
        df['trend_c'] = df.apply(convert_trend, axis=1) # Convert trend
        df['plunge_c'] = df.apply(convert_plunge, axis=1) # convert plunge

        df = df[['trend_c', 'plunge_c']] # Remove colunas antigas e fica apenas com trend e plunge
        df.columns = ['trend', 'plunge']
        print('-------------------------------\ntrend e plunge já corrigidos!!')
        return df
    else:
        print('-------------------------------\ntrend e plunge ainda não corrigidos!!')
        return df
    
def main():
    print("\nEsse programa converte as medidas de eixo-c para o sistema trend/plunge para plotagem no OpenStereo\n")
    sample = load_file(filename = str(input("Digite o nome do arquivo de entrada a ser convertido com a extensão utilizada. Por favor utilize arquivo .csv : " )), 
                       sep=';', convert=True)
    
    print('--------------------------------------- \nPreparando Exportação de dados para OpenStereo\n')
    
    sample.to_csv(str(input("Digite o nome do arquivo de saída com a extensão .txt ao final: ")),
                  sep='/', index=False)
    
    print('--------------------------------------- \nDados convertidos e exportados com sucesso!\n')
main()