from collections import defaultdict

checkers = defaultdict(lambda: 0)
for i in range(1, 25):
    checkers[i] += 0
checkers.update({1: 3, 6: 1, 10: 2, 12: 1, 13: 1})


def position_state(checkers_state, key):
    if checkers_state[key] >= 2:  # 2'den fazla pul varsa 
        return 'closed'
    elif checkers_state[key] == 0:  # Hiç pul yoksa
        return 'empty'
    elif checkers_state[key] == 1:  # Tek pul varsa
        return 'open'
    else:
        pass


def score_calculator(old_state, new_state):
    IMPORTANT_DOORS = [5, 6, 7, 8, 17, 18, 19, 20]
    score = 0
    for key in range(1, len(checkers)):
        if position_state(old_state, key) == 'empty' \
            and position_state(new_state, key) == 'empty':
            # İlk ve son hali aynı ise atlıyoruz
            continue
        elif position_state(old_state, key) == 'closed' \
                and position_state(new_state, key) == 'open':
            # İlk durumda kapalı sonra açılırsa
            if key in IMPORTANT_DOORS:
                score -= 2  # Önemli kapı ise -2
            else:
                score -= 1  # Eğer önemli kapı değilse -1
        elif position_state(old_state, key) == 'empty':
                # Eğer ilk durumda hiç pul yoksa
            if position_state(new_state, key) == 'closed':
                # Kapı kapanırsa
                if key in IMPORTANT_DOORS:
                    score += 2
                else:
                    score += 1
            elif position_state(new_state, key) == 'open':
                score -= 1  # Tek pul gelirse pul açıkta kalır
        elif position_state(old_state, key) == 'open' \
                and position_state(new_state, key) == 'closed':
            # Tek pul varsa ve 1 veya daha fazla pul gelmişse
            if key in IMPORTANT_DOORS:
                score += 2  # Önemli kapı ise
            else:
                score += 1  # Normal kapı ise
        elif position_state(old_state, key) == 'open' \
                and position_state(new_state, key) == 'empty':
            score += 1  # Tek pul varsa ve açıktan kurtarıldıysa
        else:
            pass
    return score


def get_moved_checkers(checkers_position_dice, move_pos, dice):
    # İlk konumdaki pulu 1 azaltıyorum.
    # Gelen zardaki konumda bulunan pul sayısını 1 arttırıyorum
    checkers_position_dice[move_pos], checkers_position_dice[move_pos+dice] =\
                checkers_position_dice[move_pos]-1,\
                checkers_position_dice[move_pos+dice]+1

    return checkers_position_dice


def dice(dice1, dice2):
    print("Dice {0}, {1}".format(dice1, dice2))
    print("-------------------------------------------")
    checkers_position_dice1 = checkers.copy()
    # İlk zara göre yeni dizilim oluşturmak için ilk dizilimi kopyala

    for j in checkers:
        if checkers[j] == 0:  # Pul yoksa atla
            continue
        get_moved_checkers(checkers_position_dice1, j, dice1)

        checkers_position_dice2 = checkers_position_dice1.copy()
        # İlk zarın konumuna göre ikinci zarı oynamak için
        # Oluşan durumu kopyala

        for i in checkers_position_dice1:
            # İlk zar için olan bütün kombinasyonları oyna
            if checkers_position_dice1[i] == 0:
                continue  # Eğer pul yoksa atla

            get_moved_checkers(checkers_position_dice2, i, dice2)

            score = score_calculator(checkers, checkers_position_dice2)
            if score > 0:  # Puanı 0'dan büyükse yazdır
                print(((j, j+dice1), (i, i+dice2), score))
            # Diğer kombinasyonlar için son hali kopyalar
            checkers_position_dice2 = checkers_position_dice1.copy()

        # Diğer kombinasyonlar için son hali kopyalar
        checkers_position_dice1 = checkers.copy()


def find_moves(checkers, dice1, dice2):
    dice(dice1, dice2)


find_moves(checkers, 6, 1)