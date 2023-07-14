import pygame

#image_path = '/data/data/org.game_01.myapp/files/app/'
image_path = ''
#icon = pygame.image.load(image_path+'image/icon.png').convert_alpha()
clock_game = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((1920,1023))
pygame.display.set_caption("Game_01")
icon = pygame.image.load(image_path + 'image/icon.png').convert_alpha()
pygame.display.set_icon(icon)


game_font = pygame.font.Font(image_path + 'font/AcariSans-Italic.ttf', 48)
text_menu = game_font.render('Start Game', True, 'Red')
text_lose = game_font.render('Welcome to Game_01', True, 'Blue')
text_exit = game_font.render('Exit', True, 'Blue')
text_restart = game_font.render('Играть', True, 'Red')
text_restart_rect = text_restart.get_rect(topleft=(200,250))
text_exit_rect = text_exit.get_rect(topleft=(200,300))

bullets_left = 5
bullet = pygame.image.load(image_path + 'image/bullet.png').convert_alpha()
bullets = []




#player = pygame.image.load('image/player/jump/1.png')
bg = pygame.image.load(image_path + 'image/bg.jpg').convert()
zombi = pygame.image.load(image_path + 'image/zombi.png').convert_alpha()
#zombi_x = 1920
zombi_list_in_game = []


player_run = [
    pygame.image.load(image_path + 'image/player/run/1.png').convert_alpha(),
    pygame.image.load(image_path + 'image/player/run/2.png').convert_alpha(),
    pygame.image.load(image_path + 'image/player/run/3.png').convert_alpha(),
]

player_jump = [
pygame.image.load(image_path + 'image/player/jump/1.png').convert_alpha(),
pygame.image.load(image_path + 'image/player/jump/2.png').convert_alpha(),
pygame.image.load(image_path + 'image/player/jump/4.png').convert_alpha(),

]


player_anim_count=0
bg_x =0


player_speed = 12
player_x = 300
player_y = 500
is_jump = False
jump_count = 15

bg_sound = pygame.mixer.Sound(image_path + 'sounds/bg_sound.mp3')
bg_sound.play()

zombi_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombi_timer,3000)

game_play = False
run_exit =False

run = True
while run:



    #screen.fill((200,200,200))



    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+1920, 0))
    #screen.blit(zombi, (zombi_x, 500))

    if game_play:

        player_rect = player_run[0].get_rect(topleft=(player_x,player_y))
        #zombi_rect = zombi.get_rect(topleft=(zombi_x,500))

        if zombi_list_in_game:
            for (i, el) in enumerate(zombi_list_in_game):
                screen.blit(zombi,el)
                el.x -=4

                if el.x <-10:
                    zombi_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    game_play = False
                    text_lose = game_font.render('Lose', True, 'Red')
                    text_exit = game_font.render('Exit', True, 'Red')
                    text_restart = game_font.render('Играть снова', True, 'Blue')




        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            screen.blit(player_jump[player_anim_count], (player_x, player_y))
        else:
           screen.blit(player_run[player_anim_count], (player_x, player_y))


        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -=player_speed
        elif keys[pygame.K_RIGHT] and player_x < 800:
            player_x +=player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -15:
                if jump_count >0:
                    player_y -= (jump_count**2)/2
                else:
                    player_y += (jump_count**2)/2
                jump_count -=1
            else:
                is_jump = False
                jump_count = 15



        if player_anim_count == 2:
            player_anim_count =0
        else:
            player_anim_count +=1

        bg_x -=3
        if bg_x == -1920:
            bg_x = 0




        if bullets:
            for (i,el )in enumerate(bullets):
                screen.blit(bullet, (el.x,el.y))
                el.x += 4

                if el.x > 2000:
                    bullets.pop(i)

                if zombi_list_in_game:
                    for (index, zz) in enumerate(zombi_list_in_game):
                        if el.colliderect(zz):
                            zombi_list_in_game.pop(index)
                            bullets.pop(i)


        # zombi_x -= 4

        #screen.blit(text_menu, (100, 100))
    else:
        screen.fill((100, 100, 100))
        screen.blit(text_lose,(200,200))
        screen.blit(text_restart, text_restart_rect)
        screen.blit(text_exit, text_exit_rect)

        mouse = pygame.mouse.get_pos()
        if text_restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            game_play=True
            player_y = 500
            player_x = 300
            jump_count = 15
            is_jump = False

            zombi_list_in_game.clear()
            bullets.clear()
        elif text_exit_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:

            run_exit = True






    pygame.display.update()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == zombi_timer:
            zombi_list_in_game.append(zombi.get_rect(topleft=(1920,500)))
        if game_play and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left>0:
            bullets.append(bullet.get_rect(topleft=(player_x + 20, player_y+10)))
            bullets_left -=1

        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_a:
        #        screen.fill((100, 100, 100))


    if run_exit:
        run = False
        pygame.quit()

clock_game.tick(15)

