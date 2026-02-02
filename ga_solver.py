import random
from .models import LichHoc, GiaoVien, LopHoc, PhongHoc

class GeneticScheduler:
    def __init__(self, population_size=100, generations=100):
        # Tăng số lượng quần thể lên để AI tìm phương án tốt hơn
        self.pop_size = population_size
        self.generations = generations
        
        # Lấy tất cả lớp ĐÃ MỞ
        self.lop_hocs = list(LopHoc.objects.filter(trang_thai='MO'))
        
        self.giao_viens = list(GiaoVien.objects.all())
        self.phongs = list(PhongHoc.objects.all())
        self.ca_hoc = [1, 2, 3, 4, 5, 6]
        self.thu = [2, 3, 4, 5, 6, 7, 8]

    def create_gene(self, lop_cu_the=None):
        """
        Tạo lịch cho 1 lớp cụ thể.
        Nếu không truyền lớp vào (lop_cu_the=None) thì mới random.
        """
        if not self.lop_hocs and not lop_cu_the:
            return None
            
        # Nếu có chỉ định lớp thì dùng lớp đó, không thì random
        lop = lop_cu_the if lop_cu_the else random.choice(self.lop_hocs)
        
        # Lấy giáo viên của lớp
        gv = lop.giao_vien 
        
        # Tìm phòng cùng cơ sở
        phong_phu_hop = [p for p in self.phongs if p.co_so == gv.co_so]
        
        if not phong_phu_hop:
            return None
        
        phong = random.choice(phong_phu_hop)
        
        return {
            'lop': lop, 
            'gv': gv, 
            'phong': phong,
            'thu': random.choice(self.thu),
            'ca': random.choice(self.ca_hoc)
        }

    def fitness(self, schedule):
        score = 1000
        n = len(schedule)
        
        for i in range(n):
            current = schedule[i]
            
            # 1. Kiểm tra sức chứa
            if current['lop'].hoc_viens.count() > current['phong'].suc_chua:
                score -= 500

            # 2. Kiểm tra trùng lặp
            for j in range(i + 1, n):
                other = schedule[j]
                
                # Nếu trùng Giờ (Thứ + Ca)
                if current['thu'] == other['thu'] and current['ca'] == other['ca']:
                    
                    # Trùng Giáo Viên
                    if current['gv'] == other['gv']: score -= 100
                    
                    # Trùng Phòng
                    if current['phong'] == other['phong']: score -= 100
                    
                    # Trùng Lớp (Logic an toàn)
                    if current['lop'] == other['lop']: score -= 100
                        
        return score

    def run(self):
        if not self.lop_hocs: return False

        best_schedule = []
        best_score = -99999

        for _ in range(self.pop_size):
            schedule = []
            
            # --- SỬA ĐỔI QUAN TRỌNG ---
            # Duyệt qua TỪNG LỚP trong danh sách để đảm bảo không bỏ sót lớp nào
            for lop in self.lop_hocs:
                gene = self.create_gene(lop_cu_the=lop) # Ép buộc xếp lịch cho lớp này
                if gene:
                    schedule.append(gene)
            
            if not schedule: continue

            # Chấm điểm
            score = self.fitness(schedule)
            
            if score > best_score:
                best_score = score
                best_schedule = schedule

        # Lưu kết quả
        if best_schedule:
            LichHoc.objects.all().delete()
            for item in best_schedule:
                LichHoc.objects.create(
                    lop_hoc=item['lop'],
                    phong=item['phong'],
                    thu=item['thu'],
                    ca=item['ca']
                )
            return True
        return False