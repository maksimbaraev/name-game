import pygame
import time

class VirtualKeyboard:
    def __init__(self, x, y, colors):
        self.x = x
        self.y = y
        self.colors = colors
        self.keys = {}
        self.pressed_keys = {}
        
        # Раскладка клавиатуры (ряды)
        self.key_rows = [
            list('qwertyuiop[]'),
            list('asdfghjkl;\' '),
            list('zxcvbnm,./'),
            ['space']
        ]
        
        self.create_keys()
        
    def create_keys(self):
        """Создание клавиш"""
        key_width = 50
        key_height = 50
        key_margin = 5
        
        for row_index, row in enumerate(self.key_rows):
            for col_index, key in enumerate(row):
                if key == 'space':
                    # Специальная обработка для пробела
                    x = self.x + 150
                    width = key_width * 5
                else:
                    x = self.x + col_index * (key_width + key_margin)
                    width = key_width
                
                y = self.y + row_index * (key_height + key_margin)
                
                self.keys[key] = {
                    'rect': pygame.Rect(x, y, width, key_height),
                    'char': key,
                    'pressed': False
                }
    
    def press_key(self, key_char):
        """Анимация нажатия клавиши"""
        # Обработка специальных клавиш
        if key_char == ' ':
            key_char = 'space'
        elif key_char == 'backspace':
            key_char = 'backspace'
        elif key_char == 'enter':
            key_char = 'enter'
            
        if key_char in self.keys:
            self.pressed_keys[key_char] = time.time()
            self.keys[key_char]['pressed'] = True
    
    def update(self, dt):
        """Обновление состояния клавиатуры"""
        current_time = time.time()
        # Создаем копию списка ключей для безопасного удаления
        keys_to_remove = []
        
        for key_char, press_time in self.pressed_keys.items():
            if current_time - press_time > 0.1:  # 100 мс анимация нажатия
                if key_char in self.keys:
                    self.keys[key_char]['pressed'] = False
                keys_to_remove.append(key_char)
        
        # Удаляем обработанные клавиши
        for key_char in keys_to_remove:
            del self.pressed_keys[key_char]
    
    def draw(self, screen):
        """Отрисовка клавиатуры"""
        # Фон клавиатуры
        keyboard_rect = pygame.Rect(
            self.x - 10,
            self.y - 10,
            600,  # Увеличено для всей клавиатуры
            220   # Увеличено для всех рядов
        )
        pygame.draw.rect(screen, self.colors['keyboard_bg'], keyboard_rect)
        
        # Отрисовка клавиш
        for key_char, key_data in self.keys.items():
            rect = key_data['rect']
            
            # Выбор цвета в зависимости от состояния
            if key_data['pressed']:
                color = self.colors['key_pressed']
            elif key_char == 'space':
                color = self.colors['key_special']
            else:
                color = self.colors['key_normal']
            
            # Рисуем клавишу
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Белая обводка
            
            # Рисуем символ на клавише
            font = pygame.font.Font(None, 24)
            if key_char == 'space':
                text = 'SPACE'
            else:
                text = key_char.upper()
            
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)