import itertools
import collections

poker_hand_rank = ['*', 'High Card ', 'a pair of ', 'two pair, ', 'three of a kind', 'a straight, ', 'a flush, ', 'a full house, ', 'a four of a kind', 'a straight flush', 'a royal Flush']

def get_strongest_hand_rank(dealt_card,board_card):
    '''
    ボードと手札から作れる最良役を返す

    戻り値： (役の種類、数字の並び)
    (役の種類はハイカードを1～(ロイヤル含む)ストレートフラッシュを9とする https://upswingpoker.com/poker-rules/)
    (数の並びではAは14 or 1で表記する。他は数字のまま)
    '''
    # 表記を数字,スートの形に直す
    converted_available_cards = list()
    available_cards = dealt_card + board_card

    for card in available_cards:
        card_num = card[0]
        card_suit = card[1]

        char_int = ["T","J","Q","K","A"]

        if card_num in char_int:
            card_num = 10 + char_int.index(card_num)
        else:
            card_num = int(card_num)

        converted_available_cards.append((card_num,card_suit))

    best_combination = [1,[7,5,4,3,2]]

    # 7枚から5枚選ぶ組み合わせを全て試す
    for choiced_cards in itertools.combinations(converted_available_cards,5):
        combination = get_hand_ranking(choiced_cards)

        # 作れる役と今までの最良役と比較する
        if combination[0] > best_combination[0]:
            best_combination = combination
        elif combination[0] == best_combination[0]:
            for i in range(5):
                if combination[1][i] > best_combination[1][i]:
                    best_combination = combination
                    break

    return best_combination


def get_hand_ranking(five_cards):
    '''
    5枚のカードで作れる役を返す
    '''

    suits = {"s":0,"h":0,"d":0,"c":0,}
    numbers = list()

    # スートと数字に分割
    for i in range(5):
        suits[five_cards[i][1]] += 1
        numbers.append(five_cards[i][0])

    numbers.sort(reverse=True)

    if suits["s"] == 5 or suits["h"] == 5 or suits["d"] == 5 or suits["c"] == 5:
        # 単一スート時の処理
        if numbers[0] - numbers[4] == 4:
            return [9,numbers]                      # Straight Flash
        elif numbers[0] == 14 and numbers[1] - numbers[4] == 3:
            return [9,numbers[1:] + [1]]   # Straight Flash
        else:
            return [6,numbers]  # Flash
    else:
        # 非単一スート時の処理
        counted = collections.Counter(numbers)
        cards_counts = {i:list() for i in range(5)}     # key:枚数 , value:そのカードの組み合わせ ex. card_counts[2] = [14,14,5,5]

        for k,v in counted.items():
            for i in range(v):
                cards_counts[v].append(k)

        if len(cards_counts[4]) == 1:
            return [8,cards_counts[4] + cards_counts[1]]
        elif len(cards_counts[3]) == 3:
            if len(cards_counts[2]) == 2:
                return [7,cards_counts[3] + cards_counts[2]]
            else:
                return [4,cards_counts[3] + cards_counts[1]]
        elif len(cards_counts[2]) == 4:
            return [3,cards_counts[2] + cards_counts[1]]
        elif len(cards_counts[2]) == 2:
            return [2,cards_counts[2] + cards_counts[1]]
        else:
            if numbers[0] - numbers[4] == 4:
                return [5,numbers]                      # Straight
            elif numbers[0] == 14 and numbers[1] == 5 and numbers[1] - numbers[4] == 3:
                return [5,numbers[1:]+[1]]              # Straight(wheel)
            else:
                return [1,cards_counts[1]]

hero_hand = ["Jd","7c"]
villain_hand = ["Tc","2d"]
flop = ["Qd","9d","7s"]

used_card = {"Jd","7c","Tc","2d","Qd","9d","7s"}

remain_cards = list()
for num in ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]:
    for suit in ["s","h","d","c"]:
        card = ''.join(map(str,[num,suit]))
        if card not in used_card:
            remain_cards.append(card)

cnt = 0
all_cnt = 0

for v in itertools.combinations(remain_cards,2):
    all_cnt += 1

    board_card = flop + list(v)
    hero_best_hand = get_strongest_hand_rank(hero_hand,board_card)
    villiain_best_hand = get_strongest_hand_rank(villain_hand,board_card)

    if hero_best_hand < villiain_best_hand:
        print(v,hero_best_hand,villiain_best_hand)
        cnt += 1

print(cnt,"/",all_cnt)
