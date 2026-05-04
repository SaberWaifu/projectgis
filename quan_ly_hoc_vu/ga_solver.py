import random
from .models import LopHoc, PhongHoc, GiaoVien, LichHoc, ThoiGianRanh

class GeneticScheduler:
    def run(self):
        """
        Hàm chạy thuật toán xếp lịch tự động.
        Trọng tâm: Xếp lịch DỰA TRÊN THỜI GIAN RẢNH của giáo viên.
        """
        # 1. Xóa toàn bộ lịch học cũ (Reset bảng TKB)
        LichHoc.objects.all().delete()

        # 2. Kéo dữ liệu từ Database lên RAM (Tối ưu tốc độ)
        # Chỉ xếp lịch cho những lớp đang ở trạng thái 'MO' (Đang học)
        lop_hocs = list(LopHoc.objects.filter(trang_thai='MO').select_related('giao_vien', 'giao_vien__co_so'))
        phong_hocs = list(PhongHoc.objects.select_related('co_so'))
        thoi_gian_ranh = list(ThoiGianRanh.objects.all())

        if not lop_hocs or not phong_hocs:
            return False

        # 3. Gom nhóm Thời Gian Rảnh theo từng Giáo Viên
        # Cấu trúc: { giao_vien_id: [(thu, ca), (thu, ca), ...] }
        gv_ranh_map = {}
        for t in thoi_gian_ranh:
            if t.giao_vien_id not in gv_ranh_map:
                gv_ranh_map[t.giao_vien_id] = []
            gv_ranh_map[t.giao_vien_id].append((t.thu, t.ca))

        # 4. Bộ nhớ Tạm (Trackers) để chống trùng lặp lịch
        phong_busy = {}  # Lưu trạng thái phòng: {(phong_id, thu, ca): True}
        gv_busy = {}     # Lưu trạng thái GV: {(gv_id, thu, ca): True}
        
        lich_thanh_cong = []

        # 5. Bắt đầu quá trình xếp lịch cho từng Lớp học
        for lop in lop_hocs:
            gv_id = lop.giao_vien_id
            
            # Bỏ qua nếu lớp chưa có GV, hoặc GV đó KHÔNG ĐĂNG KÝ giờ rảnh nào
            if not gv_id or gv_id not in gv_ranh_map or not gv_ranh_map[gv_id]:
                continue

            # Lọc ra các phòng: 
            # - Cùng cơ sở với giáo viên
            # - Đủ sức chứa cho sĩ số tối đa của lớp
            phong_phu_hop = [
                p for p in phong_hocs 
                if p.co_so_id == lop.giao_vien.co_so_id and p.suc_chua >= lop.si_so_toi_da
            ]

            if not phong_phu_hop:
                continue # Nếu không có phòng nào vừa, bỏ qua lớp này

            da_xep = False
            
            # Lấy danh sách GIỜ RẢNH của riêng GV này và XÁO TRỘN ngẫu nhiên
            # Xáo trộn giúp lịch học rải đều trong tuần, không dồn cục vào đầu tuần
            khung_gio_ranh = gv_ranh_map[gv_id].copy()
            random.shuffle(khung_gio_ranh)

            for thu, ca in khung_gio_ranh:
                # Kiểm tra: Trong khung giờ rảnh này, GV đã bị xếp dạy lớp khác chưa?
                if (gv_id, thu, ca) in gv_busy:
                    continue

                # Xáo trộn danh sách phòng học để dùng đều các phòng
                random.shuffle(phong_phu_hop)

                # Tìm 1 phòng trống trong khung giờ này
                for phong in phong_phu_hop:
                    if (phong.id, thu, ca) not in phong_busy:
                        
                        # ĐÃ TÌM THẤY PHƯƠNG ÁN HOÀN HẢO! -> Ghi nhận kết quả
                        lich_thanh_cong.append(LichHoc(
                            lop_hoc=lop,
                            phong=phong,
                            thu=thu,
                            ca=ca
                        ))
                        
                        # Đánh dấu Phòng và Giáo viên này đã BẬN vào giờ đó
                        phong_busy[(phong.id, thu, ca)] = True
                        gv_busy[(gv_id, thu, ca)] = True
                        
                        da_xep = True
                        break # Thoát vòng lặp phòng
                
                if da_xep:
                    break # Lớp này đã xếp xong, thoát vòng lặp thời gian để sang lớp tiếp theo

        # 6. Bulk Create: Lưu toàn bộ lịch học vào Database cùng 1 lúc (Tối ưu hiệu suất)
        if lich_thanh_cong:
            LichHoc.objects.bulk_create(lich_thanh_cong)
            return True
            
        return False