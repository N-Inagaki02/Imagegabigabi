import flet as ft
import cv2
import base64
def main(page: ft.Page):
    page.title = "pixel変換アプリ"
    page.padding = 50
    page.theme_mode = ft.ThemeMode.LIGHT
    img_original = ft.Image(fit=ft.ImageFit.CONTAIN)
    img_processed = ft.Image(fit=ft.ImageFit.CONTAIN)
    original_img_np = None
    blur_value = 1
    def process_image(img_np, blur):
        
        # ピクセル化処理
        small = cv2.resize(img_np, (12, 15), interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(small, (600, 750), interpolation=cv2.INTER_NEAREST)

        # グレースケール化
        im_gray = cv2.cvtColor(pixelated, cv2.COLOR_BGR2GRAY)

        # カラーチャンネルに戻してFletのImageで扱えるようにする（1チャンネル→3チャンネル）
        im_gray_rgb = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)

        #image出力
        cv2.imwrite('outimage.png', im_gray_rgb)

        # エンコードしてbase64に
        _, img_encoded = cv2.imencode('.png', im_gray_rgb)
        return base64.b64encode(img_encoded).decode('utf-8')

    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal original_img_np
        if e.files:
            file_path = e.files[0].path
            img_original.src = file_path
            original_img_np = cv2.imread(file_path)
            if original_img_np is None:
                print(f"Failed to load image: {file_path}")
                return
            # 画像縮小
            #original_h, original_w = original_img_np.shape[:2]
            new_width = 650
            new_height = 750
            original_img_np = cv2.resize(original_img_np, (new_width, new_height))
            # 画像サイズを取得
            height, width = original_img_np.shape[:2]
            
            # ウィンドウサイズを画像サイズに合わせて変更
            new_window_width = width * 2 + page.padding * 3  # 2つの画像 + パディング
            new_window_height = height + page.padding * 2 + 50  # 画像 + パディング + 余白(ボタンとスライダー用)
            page.window_width = new_window_width
            page.window_height = new_window_height
            
            # 画像サイズを設定
            img_original.width = width
            img_original.height = height
            img_processed.width = width
            img_processed.height = height
            
            processed_img_base64 = process_image(original_img_np, blur_value)
            img_processed.src_base64 = processed_img_base64
            page.update()
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    images_row = ft.Row(
        [img_original, img_processed],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )
    def page_resize(e):
        images_row.height = page.window_height - 100  # Adjust this value as needed
        page.update()
    page.on_resize = page_resize
    page.add(
        ft.ElevatedButton("画像を選択", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
        images_row,
    )
ft.app(target=main)