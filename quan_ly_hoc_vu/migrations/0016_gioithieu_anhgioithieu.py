from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quan_ly_hoc_vu', '0015_baitap_xinnghi_lichbu_dangkylichbu_nopbaitap_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GioiThieu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tieu_de', models.CharField(error_messages={'blank': 'Trường này không được để trống.', 'max_length': 'Đoạn văn bản này quá dài so với quy định.', 'required': 'Vui lòng nhập thông tin vào trường này.'}, max_length=200)),
                ('tom_tat', models.TextField(error_messages={'blank': 'Trường này không được để trống.', 'max_length': 'Đoạn văn bản này quá dài so với quy định.', 'required': 'Vui lòng nhập thông tin vào trường này.'})),
                ('noi_dung', models.TextField(error_messages={'blank': 'Trường này không được để trống.', 'max_length': 'Đoạn văn bản này quá dài so với quy định.', 'required': 'Vui lòng nhập thông tin vào trường này.'})),
                ('loai_muc', models.CharField(choices=[('TONG_QUAN', 'Tổng Quan'), ('SU_MENH', 'Sứ Mệnh & Giá Trị'), ('TAM_NHIN', 'Tầm Nhìn'), ('THANH_TICH', 'Thành Tích & Giải Thưởng')], default='TONG_QUAN', max_length=20)),
                ('thu_tu', models.IntegerField(default=0, help_text='Thứ tự hiển thị (số nhỏ lên trước)')),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['thu_tu', '-ngay_tao'],
            },
        ),
        migrations.CreateModel(
            name='AnhGioiThieu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hinh_anh', models.ImageField(max_length=500, upload_to='gioi_thieu/')),
                ('gioi_thieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cac_anh', to='quan_ly_hoc_vu.gioithieu')),
            ],
        ),
    ]
