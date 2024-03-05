import math
from ..util import get_direction
from game.models import Board, GameObject

class Anita(object):
    def __init__(self):
        #Menginisialisasi goal_position, previous_position, dan turn_direction
        self.goal_position = None # goal_position adalah posisi yang ingin dicapai oleh bot, dan akan diinisialisasi dengan None karena belum ada goal position
        self.previous_position = (None, None) # previous_position adalah posisi sebelumnya yang diinisialisasi dengan (None, None) karena bot belum bergerak
        self.turn_direction = 1 # turn_direction adalah arah putaran bot yang diinisialisasi dengan 1 yang berarti ke kanan

    # Fungsi ini digunakan untuk mencari diamond dengan rasio terbesar pada setiap langkahnnya
    # yang mana merupakan implementasi dari algoritma greedy
    def purge(self, board_bot: GameObject, board: Board):
        # Mendapatkan semua diamond button, diamond, dan teleporter yang ada di board dengan cara mengiterasi semua game object pada board
        # lalu mencari type yang diinginkan yakni "DiamondButtonGameObject" dan "DiamondGameObject"
        diamond_buttons = [go for go in board.game_objects if go.type == "DiamondButtonGameObject"]
        diamonds = [go for go in board.game_objects if go.type == "DiamondGameObject"]

        # Jika diamond button ada dan diamond tidak ada atau jumlah diamond kurang dari 3, maka goal position adalah diamond button pertama
        if diamond_buttons and (not diamonds or len(diamonds) < 3):
            self.goal_position = diamond_buttons[0].position
        else:
            max_ratio = -1
            min_index = None

            # Untuk setiap diamond, kalkulasi rasio dari diamond point kuadrat dengan jarak kuadrat antara bot dan diamond
            for i, diamond in enumerate (diamonds):
                bot_diamonds = board_bot.properties.diamonds # Mendapatkan jumlah diamond yang dimiliki oleh bot
                diamond_points = diamond.properties.points # Mendapatkan point dari diamond

                if (bot_diamonds + diamond_points > 5): # Jika jumlah diamond yang dimiliki bot setelah mengambil diamond ini lebih dari 5, maka skip diamond ini
                    continue

                # Melakukan kalkulasi jarak kuadrat antara bot dan diamond
                # Dengan cara mengurangi x dan y koordinat dari posisi diamond dengan posisi bot
                # Lalu hasilnya dipangkatkan 2 untuk memastikan hasilnya positif 
                x_dist = (board_bot.position.x - diamond.position.x) ** 2
                y_dist = (board_bot.position.y - diamond.position.y) ** 2
                
                # Jarak kuadrat di x dan y akhirnya dijumlahkan untuk memberikan nilai total jarak kuadrat dari bot ke diamond 
                # Teknik penentuan total jarak ini menggunakan Teorema Phytagoras
                dist_squared = x_dist + y_dist                 

                # Jika jarak kuadratnya 0, berarti bot sudah berada di posisi diamond, yang berarti
                # bot tidak lagi perlu melakukan kalkulasi ratio untuk diamond yang ini, jadi diamond yang ini akan diskip perhitungannya
                # dan akan langsung dilanjutkan ke diamond selanjutnya
                if dist_squared == 0: 
                    continue
                
                # Mengkalkulasi rasio dari diamond point kuadrat dengan jarak kuadrat dari bot ke diamond
                # Rasio ini akan digunakan untuk menentukan diamond mana yang akan dijadikan goal position
                # Diamond dengan point yang lebih tinggi dan jarak yang lebih dekat akan memiliki rasio lebih besar
                ratio = (diamond_points ** 2) / dist_squared

                # Jika rasio ini adalah rasio terbesar yang ditemukan sejauh ini, maka update max_ratio dan min_index
                # max_ratio digunakan untuk menyimpan rasio terbesar yang ditemukan sejauh ini
                # min_index digunakan untuk menyimpan index dari diamond yang memiliki rasio terbesar
                if ratio > max_ratio:
                    max_ratio = ratio
                    min_index = i

            # Jika min_index tidak None, maka kita sudah menemukan dimaond dengan rasio terbesar
            # Maka kita set goal positionnya menjadi posisi dari diamond tersebut
            if min_index is not None:
                self.goal_position = board.diamonds[min_index].position
    
    # Fungsi ini digunakan untuk menyesuaikan goal position dari bot agar dapat terhindar dari obstacle (Dalam kasus ini adalah teleporter)
    def avoid_obstacle(self, board_bot: GameObject, board: Board):
        
        # Mendapatkan semua teleporter yang ada di board dengan melakukan iterasi untuk semua game object di board
        # dan menyeleksi game object dengan type "TeleporterGameObject"
        teleporters = [go for go in board.game_objects if go.type == "TeleporterGameObject"]
        
        # Jika tidak ada teleporter di board, maka langsung return
        if not teleporters:
            return

        # Jika ada teleporter maka akan diiterasi untuk masing-masing teleporter
        for teleporter in teleporters:
            # Ini akan melakukan pengecekan apakah bot berada dalam garis lurus antara teleporter dan goal position
            if self.is_in_line(board_bot.position, teleporter.position, self.goal_position):
                # Jika mereka segaris, maka goal position bot akan disesuaikan untuk menghindari teleporter

                # Jika x koordinat dari posisi teleporter tidak sama dengan x koordinat dari posisi bot,
                # maka posisi bot dan teleporter berada pada kolom yang sama
                # Maka koordinat x dari goal position akan disesuaikan menjadi 1 langkah ke kiri atau kanan dari teleporter
                if teleporter.position.x != board_bot.position.x:
                    self.goal_position.x = teleporter.position.x - 1 if teleporter.position.x > board_bot.position.x else teleporter.position.x + 1

                # Menggunakan logika yang sama dengan penjelasan yang di atas, apabila y koordinat dari posisi teleporter tidak sama dengan y koordinat dari posisi bot
                # Maka posisi goal akan disesuaikan menjadi 1 langkah ke atas atau bawah dari teleporter
                if teleporter.position.y != board_bot.position.y:
                    self.goal_position.y = teleporter.position.y - 1 if teleporter.position.y > board_bot.position.y else teleporter.position.y + 1

    # Fungsi ini digunakan untuk mengecek apakah 3 posisi berada dalam satu garis lurus
    def is_in_line(self, pos1, pos2, pos3):
        # Mengkalkulasi perbedaan koordinat x dan y antara pos1 dan pos2
        dx1 = pos2.x - pos1.x
        dy1 = pos2.y - pos1.y

        # Setelah itu, dilakukan kalkulasi perbedaan koordinat x dan y antara pos2 dan pos3
        dx2 = pos3.x - pos2.x
        dy2 = pos3.y - pos2.y

        # Jika hasil perkalian antara dx1 dan dy2 sama dengan hasil perkalian antara dy1 dan dx2, yang berarti
        # arab dari pos1 ke pos2 dan dari pos2 ke pos3 adalah sama
        # Jadi, fungsinya akan menghasilkan true
        if dx1*dy2 == dy1*dx2:
            return True
        
        # Namun jika tidak segaris, maka fungsinya akan menghasilkan false
        return False

    # Fungsi ini digunakan untuk melakukan kalkulasi untuk gerakan selanjutnya dari bot
    def next_move(self, board_bot: GameObject, board: Board):

        # Mendapatkan properties dari bot
        props = board_bot.properties

        # Jika bot sudah mengumpulkan 5 diamond, maka goal positionnya adalah base
        if props.diamonds == 5:
            base = props.base
            self.goal_position = base
        
        else:
            # Jika belum terkumpul 5 diamond, maka akan memanggil fungsi purge untuk mencari diamond dengan rasio terbesar
            # Yang mana sudah dijelaskan fungsi purge untuk apa di atas
            self.purge(board_bot,board)
    
        # Jika bot sudah mempunyai posisi goal, maka akan dihitung gerakan untuk mendekati posisi tersebut
        if self.goal_position:
            # Akan dipanggil fungsi avoid_obstacle untuk menyesuaikan posisi goal dari bot agar dapat terhindar dari obstacle
            self.avoid_obstacle(board_bot, board)

            # Mendapatkan posisi bot sekarang
            current_position = board_bot.position
            cur_x = current_position.x
            cur_y = current_position.y

            # Memanggil fungsi get_direction untuk mendapatkan delta x dan delta y yang akan digunakan untuk bergerak dari posisi sekarang ke posisi goal
            delta_x, delta_y = get_direction(
                cur_x,
                cur_y,
                self.goal_position.x,
                self.goal_position.y,
            )

            # Jika bot tidak bergerak semenjak langkah sebelumnya, maka botnya stuck
            if (cur_x, cur_y) == self.previous_position:

                # Cara bot keluar dari posisi stuck adalah dengan mencoba mengganti arah. Misalkan arah gerak sebelumnya ada horizontal,
                # maka akan dicoba gerak secara vertikal, dan sebaliknya
                if delta_x != 0:
                    delta_y = delta_x * self.turn_direction
                    delta_x = 0
                elif delta_y != 0:
                    delta_x = delta_y * self.turn_direction
                    delta_y = 0

                # Akan mengganti arah putaran untuk langkah selanjutnya
                self.turn_direction = -self.turn_direction

            # Akan menyimpan posisi sekarang sebagai previous position untuk langkah selanjutnya
            self.previous_position = (cur_x, cur_y)

            # Akan mengembalikan delta x dan delta y yang akan digunakan untuk bergerak
            return delta_x, delta_y

        # Jika bot tidak mempunyai posisi goal, maka akan mengembalikan 0, 0 yang berarti bot tidak akan bergerak
        return 0, 0