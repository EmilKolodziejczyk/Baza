# Black Jack in Python with Pygame
import copy
import random
import pygame

# Zmienne gry
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)
pygame.init()
WIDTH, HEIGHT = 976, 582
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)
smaller_font = pygame.font.Font('freesansbold.ttf', 18)
active = False
# Win, loss, draw
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'Przekroczyłeś wynik!', 'Wygrałeś', 'Krupier wygrywa', 'Remis']

# Rozdaj karty, wybierając losowo z talii i spraw, aby funkcja działała tylko dla jednej karty
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck

# Pokaż wyniki dla gracza i krupiera na ekranie
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (WIDTH // 2 - 50, HEIGHT // 2 + 50))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (WIDTH // 2 - 50, HEIGHT // 2 - 100))

# Pokaż karty wizualnie na ekranie
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [35 + (50 * i), HEIGHT // 2 + 50 + (3 * i), 80, 140], 0, 3)
        screen.blit(font.render(player[i], True, 'black'), (40 + 50 * i, HEIGHT // 2 + 55 + 3 * i))
        screen.blit(font.render(player[i], True, 'black'), (40 + 50 * i, HEIGHT // 2 + 165 + 3 * i))
        pygame.draw.rect(screen, 'red', [35 + (50 * i), HEIGHT // 2 + 50 + (3 * i), 80, 140], 3, 3)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [35 + (50 * i), HEIGHT // 2 - 100 + (3 * i), 80, 140], 0, 3)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (40 + 50 * i, HEIGHT // 2 - 95 + 3 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (40 + 50 * i, HEIGHT // 2 + 15 + 3 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (40 + 50 * i, HEIGHT // 2 - 95 + 3 * i))
            screen.blit(font.render('???', True, 'black'), (40 + 50 * i, HEIGHT // 2 + 15 + 3 * i))
        pygame.draw.rect(screen, 'blue', [35 + (50 * i), HEIGHT // 2 - 100 + (3 * i), 80, 140], 3, 3)

# Oblicz najlepszy możliwy wynik dla ręki gracza lub krupiera
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif hand[i] == 'A':
            hand_score += 11
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

# Pokaż warunki gry i przyciski
def draw_game(act, record, result):
    button_list = []
    if not act:
        deal = pygame.draw.rect(screen, 'white', [75, 20, 200, 70], 0, 3)
        pygame.draw.rect(screen, 'green', [75, 20, 200, 70], 2, 3)
        deal_text = font.render('Start', True, 'black')
        screen.blit(deal_text, (90, 40))
        button_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, 'white', [0, HEIGHT - 150, 150, 50], 0, 3)
        pygame.draw.rect(screen, 'green', [0, HEIGHT - 150, 150, 50], 2, 3)
        hit_text = font.render('HIT', True, 'black')
        screen.blit(hit_text, (20, HEIGHT - 135))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [WIDTH - 150, HEIGHT - 150, 150, 50], 0, 3)
        pygame.draw.rect(screen, 'green', [WIDTH - 150, HEIGHT - 150, 150, 50], 2, 3)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (WIDTH - 120, HEIGHT - 135))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wygrane: {record[0]}   Przegrane: {record[1]}   Remisy: {record[2]}', True, 'white')
        screen.blit(score_text, (10, HEIGHT - 30))
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (10, 20))
        deal = pygame.draw.rect(screen, 'white', [75, HEIGHT // 2 - 50, 200, 70], 0, 3)
        pygame.draw.rect(screen, 'orange', [75, HEIGHT // 2 - 50, 200, 70], 2, 3)
        pygame.draw.rect(screen, 'orange', [77, HEIGHT // 2 - 47, 196, 64], 2, 3)
        deal_text = font.render('NOWA RĘKA', True, 'black')
        screen.blit(deal_text, (90, HEIGHT // 2 - 20))
        button_list.append(deal)
    return button_list

# Sprawdź funkcję warunków końcowych
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

# Main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    pygame.display.flip()

pygame.quit()
