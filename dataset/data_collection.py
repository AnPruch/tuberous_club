import json

from pathlib import Path

from PIL import Image
from pytesseract.pytesseract import image_to_string


def extract_data(path_to_save: Path, path_to_images: Path) -> None:
    with open(path_to_save, 'w', encoding='utf-8') as f:
        f.write('Внеучебник\n')

    for image_path in sorted(path_to_images.iterdir()):
        text = image_to_string(Image.open(image_path), lang='rus+eng')

        with open(path_to_save, 'a', encoding='utf-8') as f:
            f.write(f'\n{text}\n')


def block_data(extracted: str) -> list[tuple, ...]:
    blocks = extracted.split('\n\n')
    clear_blocks = []
    for index, block in enumerate(blocks[1:-4]):
        if not block or block == '\n' or block[0].isdigit()\
                or "EVENT" in block:
            continue
        elif '\n' in block and ('#' in block or '@' in block):
            block_lr = block.split('\n')
            if block_lr[0]:
                clear_blocks.append(' '.join(block_lr[:-1]))
            if block_lr[1]:
                clear_blocks.append(block_lr[-1])
        elif block[0].islower() or block == "GOBE" or 'собеседованиям' in block:
            clear_blocks[-1] += ' ' + block.replace('\n', ' ')
        elif block.count('\n') == 1:
            clear_blocks.append(block.replace('\n', ''))
        else:
            clear_blocks.append(block.replace('\n', ' '))

    index = clear_blocks.index('СТУАЕНЧЕСКИЙ GOBE')

    right = []
    for i in range(0, index, 4):
        right.append(tuple(clear_blocks[i:i+4]))
    for i in range(index+6, len(clear_blocks), 4):
        right.append(tuple(clear_blocks[i:i + 4]))
    right.append(tuple(clear_blocks[index:index + 3]))
    right.append(tuple(clear_blocks[index + 3:index + 6]))

    return right


def theme_data(clubs: list[tuple], themes: list) -> dict:
    data = {theme: {} for theme in themes}
    i = -2
    for index, club in enumerate(clubs):
        if index > len(clubs) - 3:
            _, contact, description = club
            data[themes[i]] = [contact, description]
            i += 1
            continue
        name, contact, theme, description = club
        if 'бизнес' in theme:
            main_tag = themes[1]
        elif 'мероприятий' in theme:
            main_tag = themes[2]
        elif 'nua' in theme:
            main_tag = themes[3]
        elif 'CCUA' in theme:
            main_tag = themes[4]
        else:
            main_tag = theme[1].upper() + theme[2:].replace('_', ' ')

        data[main_tag][name] = [contact, description]

    data[themes[-2]] = clubs[-2][1:]
    data[themes[-1]] = clubs[-1][1:]

    return data


def manual_clearing(data: dict, themes: list) -> dict:
    for theme, clubs in data.items():

        if isinstance(clubs, list):
            data[theme][0] = clubs[0].replace("@", "vk.com/")
            data[theme][1] = clubs[1].replace("УСТРОЙСТВ& образовател ьного",
                                                  "устройства образовательного")
            data[theme][1] = clubs[1].replace('СТУДСОВ&Т', 'Студсовет')
            data[theme][1] = clubs[1].replace('By3a', 'вуза')
            data[theme][1] = clubs[1].replace('иностранный студентам', "иностранным студентам")
            data[theme][1] = clubs[1].replace(' И МНОГИМмИ ', " и многими ")
            data[theme][1] = clubs[1].replace("ana", "для")
            continue

        for club_name, attr in clubs.items():
            if club_name == 'DELICE':
                clubs[club_name][0] = '@delice_hse'
                clubs[club_name][1] = attr[1].replace("нои", "но и")
            if club_name == "HSE ART,":
                clubs[club_name][0] = attr[0].replace('-', '_')
            if club_name == 'HSE MaBAND':
                clubs[club_name][0] += ', t.me/mband_hse'
            if attr[0] == '@vyshka tv':
                clubs[club_name][0] = attr[0].replace(' ', '_')
                clubs[club_name][1] = attr[1].replace('Т\\', 'TV')
            if "@novshesti" == attr[0]:
                clubs[club_name][1] = attr[1].replace('Ana Tex', 'для тех')
                clubs[club_name][1] = attr[1].replace('5 М М', "SMM")
                clubs[club_name][1] = attr[1].replace("НоВ ШЭсти", 'НоВШЭсти')
                clubs[club_name][1] = attr[1].replace('TOK', 'толк')
            if club_name == 'BOOKINEMA':
                clubs[club_name][0] = "t.me/bookinema"

            if " O " in attr[1]:
                clubs[club_name][1] = attr[1].replace(' O ', 'о')
            if 'реальны ми' in attr[1]:
                clubs[club_name][1] = attr[1].replace('реальны ми', 'реальными')
            if ' х ' in attr[1] or ' _ ' in attr[1]:
                clubs[club_name][1] = attr[1].replace(' х ', ' ')
                clubs[club_name][1] = attr[1].replace(' _ ', ' ')
            if 'HUY' in attr[1]:
                clubs[club_name][1] = attr[1].replace('HUY', "НИУ")
            if '--' in attr[1]:
                clubs[club_name][1] = attr[1].replace('--', '—')
            if '-—' in attr[1]:
                clubs[club_name][1] = attr[1].replace('-—', '—')
            if ' No ' in attr[1]:
                clubs[club_name][1] = attr[1].replace('No', 'по')
            if " He " in attr[1]:
                clubs[club_name][1] = attr[1].replace('He', "не")
            if 'Ha' in attr[1]:
                clubs[club_name][1] = attr[1].replace('Ha', 'на')
            if 'Woy' in attr[1]:
                clubs[club_name][1] = attr[1].replace('Woy', 'шоу')
            if 'BUAAT' in attr[1]:
                clubs[club_name][1] = attr[1].replace("BUAAT", 'видят')
            if "видеосотчёты" in attr[1]:
                clubs[club_name][1] = attr[1].replace('видеосотчёты', 'видеоотчёты')

            clubs[club_name][0] = attr[0].replace("@", "vk.com/")

    data[themes[0]]['HSE MUSIC BAND'] = data[themes[0]].pop('HSE МаBAND')
    data[themes[0]]['HSE DANCING CREW'] = data[themes[0]].pop('HSE DANCINGGREW')
    data[themes[0]]["HSE ART"] = data[themes[0]].pop("HSE ART,")
    data[themes[0]]['АЛЬБИОН'] = data[themes[0]].pop("ANBBHOH")
    data[themes[1]].pop('HSE ASPE®@')
    data[themes[1]]['Law Club | Юридический клуб'.upper()] = data[themes[1]].pop("LAW €LdB")
    data[themes[1]]['КЛУБ ИНТЕЛЛЕКТУАЛЬНЫХ ИГР'] = data[themes[1]].pop("_ KAYB ИНТЕЛЛЕ- uroveaer nora И ТУАЛЬНЫХ ИГР")
    data[themes[1]]['Бизнес Клуб ВШЭ'.upper()] = data[themes[1]].pop("BaSINES®GhLdB")
    data[themes[1]]['HSE Finance Club (Finclub)'.upper()] = data[themes[1]].pop("FIN@LGB HSE")
    data[themes[2]]['HSE EVENT'] = data[themes[2]].pop("HSE БУсЫ")
    data[themes[3]]['HSE LIVE'] = data[themes[3]].pop("НО lVE")
    data[themes[3]]['ВЫШКАTV'] = data[themes[3]].pop("ВЫШКАТМУ")
    data[themes[4]]["СПО «БЛИЗКИЕ ЛЮДИ»"] = data[themes[4]].pop("CHO «БЛИЗКИЕ,ЛЮДИ»")
    data[themes[4]].pop("ЗЕЛЕНАЯBbIWK A")
    data[themes[4]].pop("FEM@LaEB HSE")
    data[themes[5]]["ФУТБОЛЬНЫЙ СОЮЗ"] = data[themes[5]].pop("ФУТБОЛЬНЫЙСОЮЗ")
    data[themes[5]]["ШАХМАТНЫЙ КЛУБ"] = data[themes[5]].pop("ШАХМАТНЫЙKAYB")
    data[themes[5]]['OVERCON HSE'] = data[themes[5]].pop('OVERGONHoe')
    data[themes[5]].pop(" CAOPTHBHbIA KAYB")
    data[themes[0]]['BOOKINEMA'] = data[themes[5]].pop('BOOKINEMA')

    return data


if __name__ == "__main__":
    path_to_save = Path(__file__).parent / 'vneuchebnik.txt'
    path_to_images = Path(__file__).parent / 'vneuchebnik'
    extract_data(path_to_save, path_to_images)

    clear_path = Path(__file__).parent / 'clear_data.json'

    themes = ["Творческое начало", "Бизнес и эрудиция", "Организация мероприятий", "СМИ и медиа",
              "Большая социальная миссия", "Спорт и увлечения", "Студенческий совет", "Волонтёрский центр"]

    with open(path_to_save, 'r', encoding='utf-8') as f:
        data_str = f.read()
    clubs = block_data(data_str)
    data = theme_data(clubs, themes)

    with open(clear_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open(clear_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data = manual_clearing(data, themes)

    with open(clear_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
