import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os

st.set_page_config(layout="wide")

# PDF 파일의 페이지를 이미지로 변환하는 함수
def pdf_page_to_image(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap()
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    return img

# 파일 이름에서 확장자를 제거하는 함수
def remove_extension(file_name):
    return os.path.splitext(file_name)[0]

# Streamlit 애플리케이션
def main():
    st.title("KIWOOM HEROES")
    
    # 타자 또는 투수 선택
    option = st.radio("타자 또는 투수를 선택하세요", ('타자', '투수'))
    # PDF 및 동영상 파일이 저장된 디렉토리 경로
    
    if option == '타자':
        pdf_dir = '타자'
        video_dir = '타자_동영상'
    elif option == '투수':
        pdf_dir = '투수'
        video_dir = '투수_동영상'

    # 파일 목록 가져오기
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mov', '.avi'))]

    pdf_names = [remove_extension(f) for f in pdf_files]
    video_names = [remove_extension(f) for f in video_files]
    
    # PDF 파일 선택
    selected_pdf_name = st.selectbox("PDF 파일을 선택하세요", pdf_names)
    selected_pdf = selected_pdf_name + ".pdf"
    
    # 선수 이름 추출
    selected_player = selected_pdf_name
    
    # 해당 선수의 동영상 필터링
    player_videos = [video for video in video_files if selected_player in video]
    player_video_names = [remove_extension(v) for v in player_videos]

    # 동영상 파일 선택
    selected_video_name = st.selectbox("동영상 파일을 선택하세요", player_video_names)
    selected_video = selected_video_name + ".mp4"

    # PDF 페이지 수 가져오기
    if selected_pdf:
        pdf_path = os.path.join(pdf_dir, selected_pdf)
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count

    # 페이지 번호 선택
    selected_page = st.number_input("SELECT PAGE", min_value=1, max_value=total_pages, step=1) - 1

    # 레이아웃 설정
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("PDF 뷰어")
        if selected_pdf:
            img = pdf_page_to_image(pdf_path, selected_page)
            st.image(img, use_column_width=True)
            
    with col2:
        st.header("동영상 뷰어")
        if selected_video:
            video_path = os.path.join(video_dir, selected_video)
            st.video(video_path)

if __name__ == "__main__":
    main()
