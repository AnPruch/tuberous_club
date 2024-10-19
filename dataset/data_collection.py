"""
Data collection from "Внеучебник" via tesseract
"""
# pylint: disable=too-many-branches,too-many-statements
import json
from pathlib import Path

from PIL import Image
from pytesseract import image_to_string


def extract_data(save_path: Path, images_path: Path) -> None:
    """
    Data extraction with pytesseract.

    Args:
        save_path (pathlib.Path): Path to .txt file.
        images_path (pathlib.Path): Path to the folder with images.

    Returns:
         None: Saving extracted data to .txt file.
    """
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write('Внеучебник\n')

    for image_path in sorted(images_path.iterdir()):
        text = image_to_string(Image.open(image_path), lang='rus+eng')

        with open(save_path, 'a', encoding='utf-8') as file:
            file.write(f'\n{text}\n')


def block_data(extracted: str) -> list[tuple]:
    """
    Blocking data in tuples.

    Args:
        extracted (str): Extracted string of data.

    Returns:
        list[tuple, ...]: List of clubs' information.
    """
    blocks = extracted.split('\n\n')
    clear_blocks = []
    for index, block in enumerate(blocks[1:-4]):
        if not block or block == '\n' or block[0].isdigit()\
                or "EVENT" in block:
            continue

        if '\n' in block and ('#' in block or '@' in block):
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


def theme_data(unthemed_clubs: list[tuple], data_themes: tuple) -> dict[str, dict[str, str]]:
    """
    Dividing clubs into themes

    Args:
        clubs (list[tuple]): List of clubs' information.
        data_themes (tuple): Themes of clubs.

    Returns:
        dict: Data dictionary.
    """
    themed_data = {theme: {} for theme in data_themes}
    i = -3
    for index, club in enumerate(unthemed_clubs):
        if index > len(unthemed_clubs) - 3:
            _, contact, description = club
            name = data_themes[i].upper()
            theme = f'#{data_themes[i]}'
            i += 1
        else:
            name, contact, theme, description = club

        if 'бизнес' in theme:
            main_tag = data_themes[1]
        elif 'мероприятий' in theme:
            main_tag = data_themes[2]
        elif 'nua' in theme:
            main_tag = data_themes[3]
        elif 'CCUA' in theme:
            main_tag = data_themes[4]
        else:
            main_tag = theme[1].upper() + theme[2:].replace('_', ' ')

        themed_data[main_tag][name] = [contact, description]

    return themed_data


def manual_clearing(data: dict, themes: tuple) -> dict:
    """
    Clearing the data.

    Args:
        data (dict): Data dictionary.
        themes (tuple): Themes of clubs.

    Returns:
        dict: Data dictionary.
    """
    for theme, theme_clubs in data.items():
        if isinstance(theme_clubs, list):
            data[theme][0] = theme_clubs[0].replace("@", "vk.com/")
            data[theme][1] = theme_clubs[1].replace("УСТРОЙСТВ& образовател ьного",
                                                  "устройства образовательного")
            data[theme][1] = theme_clubs[1].replace('СТУДСОВ&Т', 'Студсовет')
            data[theme][1] = theme_clubs[1].replace('By3a', 'вуза')
            data[theme][1] = theme_clubs[1].replace('иностранный студентам',
                                                    "иностранным студентам")
            data[theme][1] = theme_clubs[1].replace(' И МНОГИМмИ ', " и многими ")
            data[theme][1] = theme_clubs[1].replace("ana", "для")
            continue

        for club_name, attr in theme_clubs.items():
            if club_name == 'DELICE':
                theme_clubs[club_name][0] = '@delice_hse'
                theme_clubs[club_name][1] = attr[1].replace("нои", "но и")
            if club_name == "HSE ART,":
                theme_clubs[club_name][0] = attr[0].replace('-', '_')
            if club_name == 'HSE МаBAND':
                theme_clubs[club_name][0] += ', t.me/mband_hse'
            if attr[0] == '@vyshka tv':
                theme_clubs[club_name][0] = attr[0].replace(' ', '_')
                theme_clubs[club_name][1] = attr[1].replace('Т\\', 'TV')
            if "@novshesti" == attr[0]:
                theme_clubs[club_name][1] = attr[1].replace('Ana Tex', 'для тех')
                theme_clubs[club_name][1] = attr[1].replace('5 М М', "SMM")
                theme_clubs[club_name][1] = attr[1].replace("НоВ ШЭсти", 'НоВШЭсти')
                theme_clubs[club_name][1] = attr[1].replace('TOK', 'толк')
            if club_name == 'BOOKINEMA':
                theme_clubs[club_name][0] = "t.me/bookinema"

            if " O " in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace(' O ', 'о')
            if 'реальны ми' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('реальны ми', 'реальными')
            if ' х ' in attr[1] or ' _ ' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace(' х ', ' ')
                theme_clubs[club_name][1] = attr[1].replace(' _ ', ' ')
            if 'HUY' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('HUY', "НИУ")
            if '--' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('--', '—')
            if '-—' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('-—', '—')
            if ' No ' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('No', 'по')
            if " He " in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('He', "не")
            if 'Ha' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('Ha', 'на')
            if 'Woy' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('Woy', 'шоу')
            if 'BUAAT' in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace("BUAAT", 'видят')
            if "видеосотчёты" in attr[1]:
                theme_clubs[club_name][1] = attr[1].replace('видеосотчёты', 'видеоотчёты')

            theme_clubs[club_name][0] = attr[0].replace("@", "vk.com/")

    data[themes[0]]['HSE MUSIC BAND'] = data[themes[0]].pop('HSE МаBAND')
    data[themes[0]]['HSE DANCING CREW'] = data[themes[0]].pop('HSE DANCINGGREW')
    data[themes[0]]["HSE ART"] = data[themes[0]].pop("HSE ART,")
    data[themes[0]]['АЛЬБИОН'] = data[themes[0]].pop("ANBBHOH")
    data[themes[1]].pop('HSE ASPE®@')
    data[themes[1]]['Law Club | Юридический клуб'.upper()] = data[themes[1]].pop("LAW €LdB")
    data[themes[1]]['КЛУБ ИНТЕЛЛЕКТУАЛЬНЫХ ИГР'] = data[themes[1]].\
        pop("_ KAYB ИНТЕЛЛЕ- uroveaer nora И ТУАЛЬНЫХ ИГР")
    data[themes[1]]['Бизнес Клуб ВШЭ'.upper()] = data[themes[1]].pop("BaSINES®GhLdB")
    data[themes[1]]['HSE Finance Club (Finclub)'.upper()] = data[themes[1]].pop("FIN@LGB HSE")
    data[themes[2]]['HSE EVENT'] = data[themes[2]].pop("HSE БУсЫ")
    data[themes[3]]['HSE LIVE'] = data[themes[3]].pop("НО lVE")
    data[themes[3]]['ВЫШКАTV'] = data[themes[3]].pop("ВЫШКАТМУ")
    data[themes[4]]["СПО «БЛИЗКИЕ ЛЮДИ»"] = data[themes[4]].pop("CHO «БЛИЗКИЕ,ЛЮДИ»")
    data[themes[4]]["ЗЕЛЁНАЯ ВЫШКА"] = data[themes[4]].pop("ЗЕЛЕНАЯBbIWK A")
    data[themes[4]].pop("FEM@LaEB HSE")
    data[themes[4]]["СЕСТРЫ"] = ["t.me/sistershse",
                                 "Клуб «Сестры» организован для женской аудитории. "
                                 "Участницы собираются для обсуждения насущных проблем,"
                                 " с которыми девушки могут столкнуться в любом возрасте. "
                                 "Сюда относят романтическую любовь, брак, male gaze,"
                                 " неуверенность в себе, перестроение своей личности "
                                 "под запросы общества, психологическое и сексуальное насилие. "
                                 "В клубе делятся своим опытом, разбирать статьи и книги,"
                                 " фильмы и объекты массовой культуры."]
    data[themes[5]]["ФУТБОЛЬНЫЙ СОЮЗ"] = data[themes[5]].pop("ФУТБОЛЬНЫЙСОЮЗ")
    data[themes[5]]["ШАХМАТНЫЙ КЛУБ"] = data[themes[5]].pop("ШАХМАТНЫЙKAYB")
    data[themes[5]]['OVERCON HSE'] = data[themes[5]].pop('OVERGONHoe')
    data[themes[5]].pop(" CAOPTHBHbIA KAYB")
    data[themes[0]]['BOOKINEMA'] = data[themes[5]].pop('BOOKINEMA')
    data[themes[8]]['BlaBlaClub'] = ['t.me/hse_speakingclub',
                                     'BlaBlaClub - это клуб, участники которого каждую неделю '
                                     'в комфортной и доброжелательной атмосфере развивают навык'
                                     'и разговорного английского языка, обсуждают интересные '
                                     'для каждого студента темы, знакомятся и находят новых '
                                     'друзей. К ним часто приходят ребята-иностранцы, которые '
                                     'делятся частичкой своей культуры и узнают больше о русской. '
                                     'Помимо классического формата встреч, они также организуют '
                                     'прогулки по городу, бранчи, кинопросмотры и пикники. '
                                     'В телеграм-канале разговорного клуба вы можете найти более '
                                     'подробную информацию, а также фотографии, которые отражают '
                                     'тепло наших встреч!']
    return data


if __name__ == "__main__":
    path_to_save = Path(__file__).parent / 'vneuchebnik.txt'
    path_to_images = Path(__file__).parent / 'vneuchebnik'
    # extract_data(path_to_save, path_to_images)

    clear_path = Path(__file__).parent / 'clear_data.json'

    club_themes = ("Творческое начало", "Бизнес и эрудиция", "Организация мероприятий",
                   "СМИ и медиа", "Большая социальная миссия", "Спорт и увлечения",
                   "Студенческий совет", "Волонтёрский центр", "Разговорные клубы")

    with open(path_to_save, 'r', encoding='utf-8') as f:
        data_str = f.read()
    clubs = block_data(data_str)
    result_data = theme_data(clubs, club_themes)

    with open(clear_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)

    with open(clear_path, 'r', encoding='utf-8') as f:
        result_data = json.load(f)

    result_data = manual_clearing(result_data, club_themes)

    with open(clear_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)
