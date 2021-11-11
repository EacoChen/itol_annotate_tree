# -*- coding: UTF-8 -*-

import pandas as pd
import plotly.express as px
import os
import re

def find_proteoclass(df):dsa
    phy_class = []
    for index, row in df.iterrows():
        phylum = row['phylum']
        tax = row['tax']
        if phylum == 'Proteobacteria':
            phy_class.append(tax.split(sep='_')[2])
            # phy_class.append(re.match(r'([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)\S*',tax).group(3))
        else:
            phy_class.append(phylum)

    df['phy/class'] = phy_class
    return df

def std_legend(title,info,sep=','):

    legend_title = title
    legend_shape = sep.join( ['1'] * len(info) )
    legend_color = sep.join( info.values() )
    legend_label = sep.join( info.keys() )

    legend_text = f"""
LEGEND_TITLE{sep}{legend_title}
LEGEND_SHAPES{sep}{legend_shape}
LEGEND_COLORS{sep}{legend_color}
LEGEND_LABELS{sep}{legend_label}"""

    return legend_text


def to_color_strip(acc2info,info2color,dataset):
    # 该部分可封装
    # 获取访问码与颜色的对应
    acc2color = {acc: info2color[phyla] for acc, phyla in acc2info.items()}

    # data 注释主体输出
    annote_text = '\n'.join(['%s,%s,%s\n' % (acc, color, acc2info[acc])  # 因为注释跟的是tax而不是phylum，所以此处没有封装
                             for acc, color in acc2color.items()])

    owned_info2color = {info:info2color[info] for acc,info in acc2info.items()}

    # legend 形成，以及整个dataset的名字
    legend_text = std_legend(dataset, owned_info2color)
    dataset_label = dataset

    # 打开模板文件
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/dataset_color_strip_template.txt').read()

    # 输入到预先修改为format格式的文本文件
    template_text = template_text.format(legend_text=legend_text,
                                         dataset_label=dataset_label)

    # 形成最后输出文件
    out_text = template_text + '\n' + annote_text

    return out_text



def to_color_style(acc2info,info2color,dataset,pos,bg=False):
    # 该部分可封装
    # 获取访问码与颜色的对应
    acc2color = {acc: info2color[phyla] for acc, phyla in acc2info.items()}
    
    if not bg:
        # data 注释主体输出
        annote_text = '\n'.join(['%s,%s,%s,1,normal' % (acc, pos, color)  
                                 for acc, color in acc2color.items()])
    else:
        annote_text = '\n'.join(['%s,%s,#ffffff,1,normal,%s' 
                                 % (acc, pos, color) 
                                 for acc, color in acc2color.items()])

    owned_info2color = {info:info2color[info] for acc,info in acc2info.items()}

    # legend 形成，以及整个dataset的名字
    legend_text = std_legend(dataset, owned_info2color)
    dataset_label = dataset

    # 打开模板文件
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/dataset_styles_template.txt').read()

    # 输入到预先修改为format格式的文本文件
    template_text = template_text.format(legend_text=legend_text,
                                         dataset_label=dataset_label)

    # 形成最后输出文件
    out_text = template_text + '\n' + annote_text

    return out_text



def to_color_range(acc2info, info2color, pos='range'):

    acc2color = {acc: info2color[phyla] for acc, phyla in acc2info.items()}
    if pos == 'range':
        anno_text = '\n'.join(['%s,%s,%s,%s' % (acc, pos, color, acc2info[acc])
                              for acc,color in acc2color.items()])
    else:
        anno_text = '\n'.join(['%s,%s,%s,normal,3' % (acc, pos, color)
                              for acc,color in acc2color.items()])
    
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/colors_styles_template.txt').read()

    # 形成最后输出文件
    out_text = template_text + '\n' + anno_text

    return out_text


def highlight_outgroup(acc2type):
    og_dict = {}
    for k, v in acc2type.items():
        if re.match(r'.*outgroup$', v):
            og_dict.update({k:v})

    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/colors_styles_template.txt').read()

    annote_text = '\n'.join(['%s label_background rgba(81,202,76,0.78)\n%s label rgba(0,0,0,1)' %(acc,acc)
                             for acc,outgroup in og_dict.items()])

    out_text = template_text + '\n' + annote_text

    return out_text

def simplebar(acc2len,name,color='#707FD1'):
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/dataset_simplebar_template.txt').read()

    bar_color = color
    dataset_label = name

    template_text = template_text.format(bar_color=bar_color,
                                         dataset_label=dataset_label)

    annote_text = '\n'.join(['%s,%d' %(acc,len) for acc,len in acc2len.items()])

    out_text = template_text + '\n' + annote_text

    return out_text


def to_binary(acc2info, label='binary', sep=','):
    shape = sep.join(range(1,len(set(list(acc2info.values())))+1))
    field_labels = sep.join(list(acc2info.values()))

    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/dataset_binary_template.txt').read()

    template_text = template_text.format(shape=shape,
                                         field_labels=field_labels,
                                         dataset_label=label)

    annotate_text = '\n'.join([sep.join([str(_) for _ in list(row)[1:]])
                               for row in df.itertuples()])

    out_text = template_text + '\n' + annotate_text

    return out_text


def to_binary_init():
    os.chdir('/share/home-user/hyc')

    genes = ['nirK', 'nirS', 'nosZ', 'norB']

    df_temp = pd.DataFrame()
    df = pd.DataFrame()

    for gene in genes:

        filepath = './work/6_ancestral_reconstruction/1_leaf_state/genome_' + gene + 'criteria.tsv'

        df_temp = pd.read_table(filepath,sep = '\t')
        df_temp.loc[df_temp[gene] == gene, [gene]] = 1
        df_temp.loc[df_temp[gene] == str('No_' + gene), [gene]] = -1
        if not df.empty:
            df = pd.merge(df, df_temp, left_on='Genome', right_on='Genome')
        else:
            df = df_temp
            continue

    # for gene in genes:
        # df.loc[df[gene] == 0, [gene]] = -1

    out_text = to_binary(df)

    with open('./work/tree/annotate/binary_annotate.txt', 'w') as f:
        f.write(out_text)

    # return df
    
def to_binary_ref(ref_ids,
                  sep = ',',
                  shape = '2',
                  field_labels = 'ref',
                  label = 'reference'):
    os.chdir('/share/home-user/hyc/db/itol_template')
    template_text = open('./dataset_binary_template.txt').read()
    template_text = template_text.format(shape=shape,
                                         field_labels=field_labels,
                                         dataset_label=label)
    annotate_text = '\n'.join(['%s%s1'%(_,sep) for _ in ref_ids])
    
    out_text = template_text + '\n' + annotate_text
    return out_text


def get_color(acc2info):
    phyla2color = {p:c for p,c in zip(sorted(set(acc2info.values())),
                                      px.colors.qualitative.T10 + px.colors.qualitative.Alphabet)}
    phyla2color['Proteobacteria']='#3C6A54'
    phyla2color['Alphaproteobacteria']='#FAD4A2'
    phyla2color['Betaproteobacteria']='#56CEFF'
    phyla2color['Gammaproteobacteria']='#98C995'
    phyla2color['Epsilonproteobacteria']='#52B6DC'
    phyla2color['Deltaproteobacteria']='#DAE8AA'
    phyla2color['Oligoflexia']='#FF8028'
    phyla2color['Candidatus Muproteobacteria'] = '#BD2B1C'
    phyla2color['Zetaproteobacteria'] = '#63680c'
    phyla2color['Actinobacteria']= '#E15F99'
    phyla2color['Bacteroidetes'] = '#DA16FF'
    phyla2color['Chloroflexi'] = '#511CFB'
    phyla2color['Cyanobacteria'] = '#00A08B'
    phyla2color['Euryarchaeota'] = '#FC0080'
    phyla2color['Firmicutes'] = '#B2828D'
    phyla2color['Gemmatimonadetes'] ='#6C7C32'
    phyla2color['Nitrospinae'] = '#862A16'
    phyla2color['Nitrospirae'] = '#A777F1'
    phyla2color['Planctomycetes'] = '#620042'
    phyla2color['Acidithiobacillia'] = '#336666'
    phyla2color['Crenarchaeota']= '#BAB0AC'
    phyla2color['Deinococcus-Thermus']= '#3283FE'
    
    return phyla2color


def to_external_label(acc2info,dataset='label info'):
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/dataset_text_template.txt').read()
    template_text = template_text.format(dataset_label = dataset)
    
    annotate_text = '\n'.join(['%s,%s,1,#000000,normal,1' %(k,v) 
                               for k,v in acc2info.items()])
    
    return template_text + '\n' + annotate_text


def label_text(acc2info):
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/labels_template.txt').read()
    
    annotate_text = '\n'.join(['%s,%s' %(k,k) 
                               for k,v in acc2info.items()])
    
    return template_text + '\n' + annotate_text


def to_popup(acc2info):
    os.chdir('/share/home-user/hyc/db/')
    template_text = open('./itol_template/popup_info_template.txt').read()
    
    annotate_text = '\n'.join(['%s,accession,%s' %(k,v) 
                               for k,v in acc2info.items()])
    
    return template_text + '\n' + annotate_text


if __name__ == '__main__':

    os.chdir('D:/eaco/Documents/protocol&method')
    # df = pd.read_excel('total_ref_outgroup.xlsx')
    # df = find_proteoclass(df)
    #
    # # extract the info you want to annotate
    # acc2phylum = dict(zip(df['version'],df['phylum']))
    #
    # # 获取总颜色，将三者统一
    # phyla2color = {p:c for p,c in zip(sorted(set(acc2phylum.values())),
    #                                   px.colors.qualitative.Dark24 + px.colors.qualitative.Light24)}
    # phyla2color['Proteobacteria']='#3C6A54'
    # phyla2color['Alphaproteobacteria']='#FAD4A2'
    # phyla2color['Betaproteobacteria']='#56CEFF'
    # phyla2color['Gammaproteobacteria']='#98C995'
    # phyla2color['Epsilonproteobacteria']='#52B6DC'
    # phyla2color['Deltaproteobacteria']='#DAE8AA'
    # phyla2color['Oligoflexia']='#FF8028'

    # 导入基因
    gene = 'nirS'
    df = pd.read_excel(gene+'_ref_outgroup.xlsx')
    df = find_proteoclass(df)

    # extract the info you want to annotate
    acc2phylum = dict(zip(df['version'],df['phylum']))
    acc2phyclas = dict(zip(df['version'],df['phy/class']))
    acc2len = dict(zip(df['version'],df['len']))
    acc2type = dict(zip(df['version'],df['type']))

    # color strip
    # out_text_phylum = to_color_strip(acc2phylum,phyla2color,'phylum')
    # out_text_phyclas = to_color_strip(acc2phyclas,phyla2color,'phylum/class')

    # label range
    # out_text = to_color_range(acc2phylum,phyla2color)

    # outgroup
    # out_text = highlight_outgroup(acc2type)

    # len
    out_text = simplebar(acc2len,'Sequence length')


    # output
    os.chdir('/share/home-user/hyc/work/5_tree/annotate/')

    # with open('./itol_annot/' + gene + '_colorstrip_phylum.txt','w') as f:
    #     f.write(out_text_phylum)

    # with open('./itol_annot/' + gene + '_colorstrip_phyclas.txt', 'w') as f:
    #     f.write(out_text_phyclas)

    with open('./' + gene + '_len.txt', 'w') as f:
        f.write(out_text)

