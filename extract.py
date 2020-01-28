import sys
import pandas as pd
import re
import warnings
import time

warnings.filterwarnings('ignore')


def parse_params(input_csv):
    try:
        df = pd.read_csv(input_csv)
        print('get {} rows'.format(len(df)))        
        saturation = '(ярко|т[её]мно|насыщенный|земельно|винно|рубиново|т-|св-|светлый|светлая|светло)'
        atyp_colors = ('(слон. кость|красное вино|вишня|синяя вода|мох|хаки|ультрамарин|'
                       'шоколад|шоколадно|хром|слоновая кость|сигнальный)')
        colors = ('(ж[её]лты[йе]|ж[её]лт\.|'
                  'зел[её]ны[йе]|зел[её]н\.|'
                  'коричневы[йе]|корич\.|'
                  'красны[йе]|красн\.|'
                  'сини[йе]|син\.|'
                  'белы[йе]|бел\.|'
                  'серы[йе]|сер\.|'
                  'черны[йе]|ч[её]рн\.|'
                  'золотой?|зол\.)')
        df['color'] = df['title'].str.extract(colors, re.IGNORECASE)
        df['color'][df['color'].isnull()] = ''
        df['atype_colors'] = df['title'].str.extract(atyp_colors, re.IGNORECASE)
        df['atype_colors'][df['atype_colors'].isnull()] = ''
        df['saturation'] = df['title'].str.extract(saturation, re.IGNORECASE)
        df['saturation'][df['saturation'].isnull()] = ''
        df['color'] = (df['saturation'] + ' ' + df['atype_colors'] + ' ' + df['color']).str.normalize('NFC').str.strip()        
        df[['diameter', 'length']] = df['title'].str.replace(',', '.').str.extract(
            '(\d+\.?\d*)\s?[xх*\/]\s?(\d+\.?\d*)', re.IGNORECASE).astype(float)
        df.set_index('id', inplace=True)
        df.drop(['atype_colors', 'saturation', 'title'], axis=1, inplace=True)
        df.to_csv('out-attributes.csv')
        print("parse {} colors, {} diameters, {} lengths".format(df['color'][df['color'] != ''].count(), df['diameter']
              [df['diameter'] != ''].count(), df['length'][df['length'] != ''].count()))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_time = time.time()
        parse_params(sys.argv[1])
        print('completed in %s seconds' % (time.time() - start_time))
    else:
        print('specify the input file in the launch options')
        sys.exit(1)
