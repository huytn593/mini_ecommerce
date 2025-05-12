// Cấu hình API client
const API_URL = 'http://localhost:8000';

class ApiClient {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': this.token ? `Bearer ${this.token}` : ''
        };
    }

    async login(email, password) {
        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Đăng nhập thất bại');
            }

            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify({
                id: data.user_id,
                username: data.username,
                role: data.role
            }));

            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Đăng ký thất bại');
            }

            return data;
        } catch (error) {
            console.error('Register error:', error);
            throw error;
        }
    }

    async getProducts(category = null, sort = null, limit = 10, skip = 0) {
        try {
            let url = `${API_URL}/products?limit=${limit}&skip=${skip}`;

            if (category) {
                url += `&category=${encodeURIComponent(category)}`;
            }

            if (sort) {
                url += `&sort=${sort}`;
            }

            const response = await fetch(url, {
                method: 'GET',
                headers: this.getHeaders()
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Không thể lấy danh sách sản phẩm');
            }

            return data;
        } catch (error) {
            console.error('Get products error:', error);
            throw error;
        }
    }

    async searchProducts(query) {
        try {
            const url = `${API_URL}/products/search?q=${encodeURIComponent(query)}`;

            const response = await fetch(url, {
                method: 'GET',
                headers: this.getHeaders()
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Tìm kiếm thất bại');
            }

            return data;
        } catch (error) {
            console.error('Search products error:', error);
            throw error;
        }
    }

    async getProductById(id) {
        try {
            const response = await fetch(`${API_URL}/products/${id}`, {
                method: 'GET',
                headers: this.getHeaders()
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Không thể lấy thông tin sản phẩm');
            }

            return data;
        } catch (error) {
            console.error('Get product error:', error);
            throw error;
        }
    }

    async getUserProfile() {
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                method: 'GET',
                headers: this.getHeaders()
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Không thể lấy thông tin người dùng');
            }

            return data;
        } catch (error) {
            console.error('Get user profile error:', error);
            throw error;
        }
    }

    async updateUserProfile(profileData) {
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(profileData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Cập nhật thông tin thất bại');
            }

            return data;
        } catch (error) {
            console.error('Update profile error:', error);
            throw error;
        }
    }

    async getCart() {
        try {
            const response = await fetch(`${API_URL}/cart`, {
                method: 'GET',
                headers: this.getHeaders()
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Không thể lấy giỏ hàng');
            }

            return data;
        } catch (error) {
            console.error('Get cart error:', error);
            throw error;
        }
    }

    async addToCart(productId, quantity) {
        try {
            const response = await fetch(`${API_URL}/cart/add`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Không thể thêm vào giỏ hàng');
            }

            return data;
        } catch (error) {
            console.error('Add to cart error:', error);
            throw error;
        }
    }
}

// Xuất API client để sử dụng trong các file JS khác
const apiClient = new ApiClient();