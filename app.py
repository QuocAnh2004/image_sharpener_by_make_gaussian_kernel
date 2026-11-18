import numpy as np
import streamlit as st
from PIL import Image

MAX_SIDE = 400  # Vòng for Python chậm → thu nhỏ ảnh trước khi xử lý


def make_gaussian_kernel(size: int, sigma: float) -> np.ndarray:
    """Tạo Gaussian kernel 2D, tổng các phần tử = 1."""
    x = np.arange(-(size // 2), size // 2 + 1)
    g = np.exp(-x**2 / (2 * sigma**2))
    kernel_2d = np.outer(g, g)
    return kernel_2d / kernel_2d.sum()


def convolve2d(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Tích chập 1 kênh màu với kernel."""
    k = kernel.shape[0]
    height, width = channel.shape
    padded = np.pad(channel, k // 2, mode="edge")
    output = np.zeros_like(channel, dtype=np.float64)

    for i in range(height):
        for j in range(width):
            window = padded[i:i + k, j:j + k]
            output[i, j] = np.sum(window * kernel)
    return output


def gaussian_blur(image: np.ndarray, size: int, sigma: float) -> np.ndarray:
    """Làm mờ ảnh RGB bằng Gaussian kernel, xử lý từng kênh màu."""
    kernel = make_gaussian_kernel(size, sigma)
    channels = [convolve2d(image[:, :, c], kernel) for c in range(3)]
    return np.stack(channels, axis=2)


def unsharp_mask(image: np.ndarray, size: int, sigma: float, amount: float) -> np.ndarray:
    """Làm nét ảnh: ảnh gốc + amount * (ảnh gốc - ảnh mờ)."""
    blurred = gaussian_blur(image, size, sigma)
    sharp = image + amount * (image - blurred)
    return np.clip(sharp, 0, 255).astype(np.uint8)


def load_image(uploaded_file) -> np.ndarray:
    """Đọc ảnh upload, chuyển RGB và thu nhỏ về tối đa MAX_SIDE pixel."""
    img = Image.open(uploaded_file).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    return np.asarray(img, dtype=np.float64)


def main() -> None:
    st.title("Batoluxi · Image Sharpener")
    uploaded = st.file_uploader("Upload ảnh", type=["jpg", "jpeg", "png"])
    size = st.sidebar.slider("Kernel size", 3, 15, 5, step=2)
    sigma = st.sidebar.slider("Sigma", 0.5, 5.0, 1.0)
    amount = st.sidebar.slider("Amount (độ nét)", 0.0, 3.0, 1.0)

    if uploaded is None:
        st.info("Chọn 1 ảnh để bắt đầu.")
        return

    image = load_image(uploaded)
    with st.spinner("Đang xử lý..."):
        result = unsharp_mask(image, size, sigma, amount)

    col_before, col_after = st.columns(2)
    col_before.image(image.astype(np.uint8), caption="Gốc")
    col_after.image(result, caption="Sau khi làm nét")


if __name__ == "__main__":
    main()
