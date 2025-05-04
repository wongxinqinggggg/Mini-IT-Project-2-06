import pygame
import random
import sys
energy = int(sys.argv[1]) if len(sys.argv) > 1 else 50
money = int(sys.argv[2]) if len(sys.argv) > 2 else 0

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Supermarket Cashier Game")

# 时钟
clock = pygame.time.Clock()
FPS = 60

# 加载并缩放图像
def load_and_scale(image_path):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (WIDTH, HEIGHT))

menu_img = load_and_scale("MG2-Menu.png")
instruction_img = load_and_scale("MG2-Instructions.png")
success_img = load_and_scale("MG2-Success.png")
fail_img = load_and_scale("MG2-Fail.png")
element_img = load_and_scale("main_element.png")

# 加载并缩放收据图像
receipt_imgs = [
    pygame.transform.scale(pygame.image.load(f"MG2-Game{i}.png"), (WIDTH, HEIGHT)) for i in range(1, 11)
]

# 字体
font = pygame.font.SysFont(None, 48)

# 游戏变量
game_state = "menu"  # menu, instruction, playing, success, fail
current_receipt = None
order_left = 5
time_left = 30
input_text = ""
correct_amount = 0

# 收据对应的正确金额
receipt_answers = {
    0: 3.50,
    1: 8.00,
    2: 6.00,
    3: 7.50,
    4: 8.30,
    5: 45.10,
    6: 15.20,
    7: 66.00,
    8: 1.30,
    9: 9.00
}

# 定时器事件
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)

# 函数定义
def reset_game():
    global order_left, time_left, input_text
    order_left = 5
    time_left = 30
    input_text = ""
    next_order()

def next_order():
    global current_receipt, correct_amount, input_text
    idx = random.randint(0, 9)
    current_receipt = receipt_imgs[idx]
    correct_amount = receipt_answers[idx]
    input_text = ""

# 主循环
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(main_element.png, (10, 10))
    screen.blit(energy_text, (30, 30))
    screen.blit(money_text, (30, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if game_state == "menu":
                # 开始游戏按钮区域
                if 400 <= mouse_x <= 600 and 300 <= mouse_y <= 480:
                    reset_game()
                    game_state = "playing"
                # 说明页面按钮区域（右下角）
                if 924 <= mouse_x <= 1004 and 20 <= mouse_y <= 100:
                    game_state = "instruction"

            elif game_state == "instruction":
                # 点击任意位置返回菜单
                game_state = "menu"

        if event.type == pygame.KEYDOWN and game_state == "playing":
            if event.key == pygame.K_RETURN:
                try:
                    if abs(float(input_text) - correct_amount) < 0.01:
                        order_left -= 1
                        if order_left == 0:
                            game_state = "success"
                        else:
                            next_order()
                    else:
                        game_state = "fail"
                except:
                    pass
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isdigit() or event.unicode == '.':
                    input_text += event.unicode

        if event.type == TIMER_EVENT and game_state == "playing":
            time_left -= 1
            if time_left <= 0:
                game_state = "fail"

    # 渲染不同的游戏状态
    if game_state == "menu":
        screen.blit(menu_img, (0, 0))

    elif game_state == "instruction":
        screen.blit(instruction_img, (0, 0))

    elif game_state == "playing":
        screen.blit(current_receipt, (0, 0))

        # 显示剩余订单数
        order_text = font.render(f"Order Left: {order_left}", True, (0, 0, 0))
        screen.blit(order_text, (20, 20))

        # 显示剩余时间
        time_text = font.render(f"Time: {time_left}", True, (0, 0, 0))
        screen.blit(time_text, (WIDTH - 200, 20))

        # 显示输入框
        input_surface = font.render(input_text, True, (0, 0, 0))
        input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        pygame.draw.rect(screen, (200, 200, 200), input_rect.inflate(20, 20))
        screen.blit(input_surface, input_rect)

    elif game_state == "success":
        screen.blit(success_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        game_state = "menu"

    elif game_state == "fail":
        screen.blit(fail_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        game_state = "menu"

        def save_result():
            success = {
                "energy": energy,
                "money": money
            }
            with open("minigame_result.json", "w") as f:
                json.dump(result, f)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
