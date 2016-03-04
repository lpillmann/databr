# coding: utf-8
import pandas as pd
import db_functions as db

# df = pd.DataFrame(columns=('PRNV', 'Sim', 'Nao', 'LS', 'MIS', 'Outro'))
# df.loc[0] = [1,2,3,4,5,6]
# df
# df.loc['senadorX'] = [6,5,4,3,2,1]
    
def get_dict_qtde_votos():

    dict_senadores = db.get_dict_nomes_senadores()
    qtde_votos_dict = {}
    for codigo, nome in dict_senadores.iteritems():
        #inicializa dict interno com zeros por padrão
        qtde_votos_dict[str(codigo)] = {
            'Nome'  : '',
            'Sim'   : 0,
            'Nao'   : 0,
            'PNRV'  : 0,
            'MIS'   : 0,
            'LS'    : 0,
            'LL'    : 0,
            'Outro' : 0
        } 
        votos = db.get_votos_senador(codigo)
        
        for key, val in votos.iteritems():
            qtde_votos_dict[str(codigo)]['Nome'] = nome
            qtde_votos_dict[str(codigo)][key] = len(val)
            #print key, len(val)

    return qtde_votos_dict    

# Dict construído. Converter para DataFrame
def get_table_qtde_votos(q_votos_dict):
    
    df = pd.DataFrame(columns=( 
                            'Sim'  ,
                            'Nao'  ,
                            'PNRV' ,
                            'MIS'  ,
                            'LS'   ,
                            'LL'   ,
                            'Outro'))

    for key, val in q_votos_dict.iteritems():
        df.loc[val['Nome']] = [
                                val['Sim'  ],
                                val['Nao'  ],
                                val['PNRV' ],
                                val['MIS'  ],
                                val['LS'   ],
                                val['LL'   ],
                                val['Outro']]

    print df






