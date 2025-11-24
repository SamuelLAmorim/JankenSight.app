from ultralytics import YOLO
import cv2
import random
import time
from utils.game_logic import determine_winner, Score

# --- CONFIGURAÇÕES GLOBAIS ---
MODEL_PATH = 'models/best.pt' 
CONFIDENCE_THRESHOLD = 0.7 
COUNTDOWN_TIME = 3 

# --- CONFIGURAÇÕES VISUAIS E ESTADOS ---
WINDOW_NAME = 'YOLOv8 Jokenpo Game'
COLOR_BACKGROUND = (100, 100, 100)
COLOR_WINNER = (0, 255, 0)
COLOR_LOSER = (0, 0, 255)
COLOR_TIE = (255, 255, 0)
COLOR_BUTTON = (50, 50, 200) 
FONT = cv2.FONT_HERSHEY_TRIPLEX
FONT_SCALE = 1
THICKNESS = 2

# Variáveis de estado global para a interação
IS_PAUSED = False
IS_RUNNING = True
IS_FULLSCREEN = True 
W, H = 1280, 720 
MARGIN = 20 # Margem constante

# --- Funções Auxiliares (Desenho) ---

def draw_text_box(frame, text, position, color, bg_color=COLOR_BACKGROUND):
    """Desenha um texto com um retângulo de fundo para melhor visibilidade."""
    x, y = position
    (text_w, text_h), baseline = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)
    
    cv2.rectangle(frame, (x, y - text_h - 10), (x + text_w + 10, y + baseline + 10), bg_color, -1)
    cv2.putText(frame, text, (x + 5, y + 5), FONT, FONT_SCALE, color, THICKNESS)

def draw_button(frame, text, rect_pos, color=(255, 255, 255)):
    """Desenha um botão com texto centralizado."""
    x, y, w, h = rect_pos
    cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR_BUTTON, -1)
    
    (text_w, text_h), baseline = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)
    text_x = x + int((w - text_w) / 2)
    text_y = y + int((h + text_h) / 2)
    
    cv2.putText(frame, text, (text_x, text_y), FONT, FONT_SCALE, color, THICKNESS)


# --- Função de Callback do Mouse (Apenas Lógica de Clique!) ---

def mouse_callback(event, x, y, flags, param):
    """
    Função chamada quando um evento de mouse ocorre. APENAS MANIPULA O CLIQUE.
    """
    global IS_PAUSED, IS_RUNNING, IS_FULLSCREEN, W, H, MARGIN

    # Dimensões REDUZIDAS para botões
    BUTTON_H = 45
    BUTTON_W = 120
    
    # Posição do botão PAUSE (Centralizado)
    pause_rect = (int(W/2 - BUTTON_W/2), MARGIN, BUTTON_W, BUTTON_H)
    px, py, pw, ph = pause_rect
    
    # Posição do botão MINIMIZAR (Esquerdo)
    minimize_rect = (MARGIN, MARGIN, 150, BUTTON_H) # Largura ajustada
    mx, my, mw, mh = minimize_rect

    # Posição do botão SAIR (Direito)
    exit_rect = (W - BUTTON_W - MARGIN, MARGIN, BUTTON_W, BUTTON_H)
    ex, ey, ew, eh = exit_rect

    if event == cv2.EVENT_LBUTTONDOWN:
        # Checa clique no botão PAUSE
        if px <= x <= px + pw and py <= y <= py + ph:
            IS_PAUSED = not IS_PAUSED
            
        # Checa clique no botão MINIMIZAR/FULLSCREEN
        elif mx <= x <= mx + mw and my <= y <= my + mh:
            IS_FULLSCREEN = not IS_FULLSCREEN
        
        # Checa clique no botão SAIR
        elif ex <= x <= ex + ew and ey <= y <= ey + eh:
            IS_RUNNING = False 


# --- Lógica de Detecção (Inalterada) ---

def detect_player_move(results, class_names, frame_width):
    best_conf = 0.0
    best_move = None
    PLAYER_ZONE_LIMIT = frame_width / 2

    for r in results:
        for box in r.boxes:
            conf = box.conf.item()
            cls_id = int(box.cls.item())
            predicted_class = class_names[cls_id]
            x_center = box.xywh[0][0].item()
            
            if x_center < PLAYER_ZONE_LIMIT and conf > best_conf:
                best_conf = conf
                best_move = predicted_class
                
    return best_move


# --- Loop Principal do Jogo ---

def run_game():
    global IS_PAUSED, IS_RUNNING, IS_FULLSCREEN, W, H, MARGIN

    try:
        model = YOLO(MODEL_PATH)
        class_names = model.names
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}. Verifique o caminho: {MODEL_PATH}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return
        
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    score = Score()
    start_time = time.time()
    current_winner = "Pronto para jogar! (Pressione P para Pause)"
    player_move = None
    ia_move = None
    previous_fullscreen_state = None

    while IS_RUNNING:
        
        # LÓGICA DE SUSPENSÃO/MINIMIZAÇÃO DA TELA CHEIA
        if IS_FULLSCREEN != previous_fullscreen_state:
            if IS_FULLSCREEN:
                cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                W, H = 1920, 1080 
            else:
                cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(WINDOW_NAME, 800, 600) 
                W, H = 800, 600
            previous_fullscreen_state = IS_FULLSCREEN
        
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1) 
        frame = cv2.resize(frame, (W, H))
        FRAME_CENTER_X = int(W / 2)


        # --- LÓGICA DE PAUSA ---
        if IS_PAUSED:
            draw_text_box(frame, "PAUSADO", (FRAME_CENTER_X - 100, H // 2 - 50), (255, 255, 255), (0, 0, 0))
        else:
            # --- Lógica do Jogo ---
            
            elapsed_time = time.time() - start_time
            countdown_left = COUNTDOWN_TIME - int(elapsed_time)
            
            # ZONAS DE JOGO (NOVO POSICIONAMENTO: Cantos Inferiores)
            cv2.line(frame, (FRAME_CENTER_X, 0), (FRAME_CENTER_X, H), (255, 255, 255), 3)
            
            # Altura do Placar para calcular a posição Y da Zona
            SCORE_BOX_H_DEFAULT = 100
            ZONE_Y_POS = H - SCORE_BOX_H_DEFAULT - MARGIN - 40 # 40px acima do placar

            # SUA ZONA (Canto Inferior Esquerdo)
            draw_text_box(frame, "SUA ZONA", (MARGIN, ZONE_Y_POS), (255, 255, 255))
            
            # IA/OPONENTE (Canto Inferior Direito)
            # Calculamos a largura do texto da IA para ancorar na direita
            text_ia_w, _ = cv2.getTextSize("IA/OPONENTE", FONT, FONT_SCALE, THICKNESS)[0]
            ia_x_pos = W - text_ia_w - MARGIN - 10 # 10px para dar espaço à caixa de texto
            draw_text_box(frame, "IA/OPONENTE", (ia_x_pos, ZONE_Y_POS), (255, 255, 255))

            if countdown_left > 0:
                countdown_text = f"PREPARE: {countdown_left}"
                draw_text_box(frame, countdown_text, (FRAME_CENTER_X - 100, 200), (0, 255, 255))
                player_move = None
                ia_move = None
            else:
                results = model.predict(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
                player_move = detect_player_move(results, class_names, W)
                frame = results[0].plot(boxes=True, labels=True)

                if player_move:
                    ia_move = random.choice(list(class_names.values())) 
                    result = determine_winner(player_move, ia_move)
                    score.update(result)
                    current_winner = result
                    start_time = time.time()
            
            # --- Exibição de Feedback de Jogadas e Vencedor ---
            if 'Wins' in current_winner:
                result_color = COLOR_WINNER if 'Player 1' in current_winner else COLOR_LOSER
            elif 'Tie' in current_winner:
                result_color = COLOR_TIE
            else:
                result_color = (255, 255, 255)
                
            draw_text_box(frame, current_winner, (FRAME_CENTER_X - 150, 50), result_color)
            
            if player_move:
                draw_text_box(frame, f"VOCE: {player_move.upper()}", (30, 100), COLOR_WINNER)
            
            if ia_move:
                draw_text_box(frame, f"IA: {ia_move.upper()}", (FRAME_CENTER_X + 30, 100), COLOR_LOSER)
        
        
        # --- Desenha Botões (Sempre Visíveis e Centralizados) ---
        
        BUTTON_W = 120 # Menor
        BUTTON_H = 45  # Menor
        
        # Centralizado: PAUSE/RETOMAR
        pause_text = "PAUSE" if not IS_PAUSED else "RETOMAR"
        draw_button(frame, pause_text, (int(W/2 - BUTTON_W/2), MARGIN, BUTTON_W, BUTTON_H)) 

        # Esquerda: MINIMIZAR/FULLSCREEN
        fullscreen_text = "MINIMIZAR (F)" if IS_FULLSCREEN else "TELA CHEIA (F)"
        draw_button(frame, fullscreen_text, (MARGIN, MARGIN, 150, BUTTON_H)) 

        # Direita: SAIR
        draw_button(frame, "SAIR (Q)", (W - BUTTON_W - MARGIN, MARGIN, BUTTON_W, BUTTON_H)) 

        
        # 💥 PLACAR APRIMORADO (CENTRALIZADO INFERIOR) 💥
        
        p1_score, p2_score = score.get_scores()
        
        # Dimensões do Placar
        SCORE_BOX_W = 400
        SCORE_BOX_H = 100
        
        # NOVO CÁLCULO X: Centralizado
        SCORE_BOX_X = FRAME_CENTER_X - int(SCORE_BOX_W / 2) 
        SCORE_BOX_Y = H - SCORE_BOX_H - MARGIN # MARGIN acima da borda inferior

        # 1. Retângulo de Fundo Principal do Placar (Cinza Escuro)
        cv2.rectangle(frame, 
                      (SCORE_BOX_X, SCORE_BOX_Y), 
                      (SCORE_BOX_X + SCORE_BOX_W, SCORE_BOX_Y + SCORE_BOX_H), 
                      (50, 50, 50), -1)
        
        # Ponto central X do placar para o divisor e alinhamento do texto
        SCORE_CENTER_X = SCORE_BOX_X + int(SCORE_BOX_W / 2)
        
        # 2. Divisor Central
        cv2.line(frame, 
                 (SCORE_CENTER_X, SCORE_BOX_Y), 
                 (SCORE_CENTER_X, SCORE_BOX_Y + SCORE_BOX_H), 
                 (255, 255, 255), 2)

        # 3. Textos do Placar
        
        # --- Jogador 1 (VOCÊ) - Esquerda da caixa ---
        cv2.putText(frame, "VOCE", 
                    (SCORE_BOX_X + 10, SCORE_BOX_Y + 30), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (200, 200, 255), 1)
        cv2.putText(frame, str(p1_score), 
                    (SCORE_BOX_X + 50, SCORE_BOX_Y + 85), 
                    cv2.FONT_HERSHEY_DUPLEX, 2.0, COLOR_WINNER, 4)

        # --- Jogador 2 / IA - Direita da caixa ---
        cv2.putText(frame, "I.A.", 
                    (SCORE_CENTER_X + 10, SCORE_BOX_Y + 30), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 200, 200), 1)
        cv2.putText(frame, str(p2_score), 
                    (SCORE_CENTER_X + 50, SCORE_BOX_Y + 85), 
                    cv2.FONT_HERSHEY_DUPLEX, 2.0, COLOR_LOSER, 4)

        # Contorno da caixa do placar
        cv2.rectangle(frame, 
                      (SCORE_BOX_X, SCORE_BOX_Y), 
                      (SCORE_BOX_X + SCORE_BOX_W, SCORE_BOX_Y + SCORE_BOX_H), 
                      (255, 255, 255), 3)
        # Fim do novo placar
        
        cv2.imshow(WINDOW_NAME, frame)

        # 4. Comandos de Teclado
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            IS_RUNNING = False
        if key == ord('p'):
            IS_PAUSED = not IS_PAUSED
        if key == ord('f'):
            IS_FULLSCREEN = not IS_FULLSCREEN


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run_game()