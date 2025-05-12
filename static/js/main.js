// Global variables
const API_URL = 'http://localhost:8000';
let currentUser = null;

// DOM Ready
$(document).ready(function() {
    // Initialize
    init();
    
    // Setup event handlers
    setupEventHandlers();
});

// Initialize the application
function init() {
    // Check if user is logged in
    checkAuth();
    
    // Setup navigation
    updateNavigation();
    
    // Load page specific content
    loadPageContent();
}

// Check authentication status
function checkAuth() {
    const token = localStorage.getItem('token');

    if (token) {
        // Get user info from token
        const user = parseJwt(token);
        currentUser = {
            id: user.sub,
            username: user.username,
            role: user.role
        };

        // Update UI for logged in user
        $('#authButtons').hide();
        $('#userProfile').show();
        $('#username').text(currentUser.username);

        // Show role specific elements
        $(`.role-${currentUser.role}`).show();

        // Setup profile dropdown
        setupProfileDropdown();
    } else {
        // Update UI for guest
        $('#authButtons').show();
        $('#userProfile').hide();
        $('.role-specific').hide();
    }

    // Cập nhật badge giỏ hàng
    updateCartBadge();
}

// Update navigation based on page and auth
function updateNavigation() {
    // Get current page from URL
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    // Add active class to current page link
    $(`.nav-link[href="${currentPage}"]`).addClass('active');
    
    // Handle restricted pages
    if (!currentUser) {
        // Redirect from restricted pages to login
        if (
            currentPage === 'seller_dashboard.html' ||
            currentPage === 'admin_dashboard.html' ||
            currentPage === 'cart.html'
        ) {
            window.location.href = 'login.html?redirect=' + currentPage;
        }
    } else {
        // Redirect from role-specific pages if not authorized
        if (currentPage === 'seller_dashboard.html' && currentUser.role !== 'seller' && currentUser.role !== 'admin') {
            window.location.href = 'index.html';
        }
        if (currentPage === 'admin_dashboard.html' && currentUser.role !== 'admin') {
            window.location.href = 'index.html';
        }
    }
}

// Load page specific content
function loadPageContent() {
    // Get current page from URL
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    // Load page specific content
    switch (currentPage) {
        case 'index.html':
            loadProducts();
            break;
        case 'product_detail.html':
            loadProductDetail();
            break;
        case 'cart.html':
            loadCart();
            break;
        case 'seller_dashboard.html':
            loadSellerDashboard();
            break;
        case 'admin_dashboard.html':
            loadAdminDashboard();
            break;
    }
}
// Toggle profile page
function toggleProfilePage(show) {
    const profilePage = $('#profilePage');
    if (show) {
        profilePage.show();
        // Scroll to profile page
        $('html, body').animate({
            scrollTop: profilePage.offset().top
        }, 500);
    } else {
        profilePage.hide();
    }
}

// Thêm hàm để lưu profile
function saveProfile() {
    if (!currentUser) return;

    const name = $('#profileName').val();
    const gender = $('input[name="gender"]:checked').val();
    const birthday = $('#profileBirthday').val();

    // Gọi API để lưu thông tin profile (giả lập)
    // Trong thực tế, bạn sẽ gửi request đến backend
    setTimeout(() => {
        showAlert('Đã lưu thông tin thành công!', 'success');
        toggleProfilePage(false);
    }, 500);
}

// Setup event handlers
function setupEventHandlers() {
    // Giữ lại các handler hiện có

    // Thêm handler mới cho nút tìm kiếm
    $('#searchForm').on('submit', function(e) {
        e.preventDefault();
        const query = $('#searchInput').val().trim();
        if (query) {
            window.location.href = `/search.html?q=${encodeURIComponent(query)}`;
        }
    });

    // Thêm handler cho nút tìm kiếm
    $('.search-button').on('click', function() {
        const query = $('#searchInput').val().trim();
        if (query) {
            window.location.href = `/search.html?q=${encodeURIComponent(query)}`;
        }
    });

    // Thêm handler cho profile page
    $('#editProfileBtn').on('click', function() {
        toggleProfilePage(true);
    });

    $('#closeProfileBtn').on('click', function() {
        toggleProfilePage(false);
    });

    $('#saveProfileBtn').on('click', function() {
        saveProfile();
    });
}
// Xử lý dropdown tài khoản
function setupProfileDropdown() {
    const profileTrigger = $('.profile-trigger');

    profileTrigger.on('click', function() {
        const dropdownContent = $(this).siblings('.dropdown-content');
        dropdownContent.toggleClass('show');

        // Đóng dropdown khi click ra ngoài
        $(document).on('click', function(event) {
            if (!$(event.target).closest('.profile-dropdown').length) {
                $('.dropdown-content').removeClass('show');
            }
        });
    });

    // Xử lý khi click vào nút đăng xuất
    $('#logoutButton').on('click', function() {
        logout();
    });

    // Hiển thị avatar
    if (currentUser) {
        const userAvatar = $('#userAvatar');
        // Nếu có avatar thì hiển thị, nếu không thì hiển thị chữ cái đầu
        if (currentUser.avatar) {
            userAvatar.html(`<img src="${currentUser.avatar}" alt="Avatar">`);
        } else {
            const initial = currentUser.username.charAt(0).toUpperCase();
            userAvatar.text(initial);
        }
    }
}
// Cập nhật hàm checkAuth để tương thích với thiết kế mới
function checkAuth() {
    const token = localStorage.getItem('token');

    if (token) {
        // Get user info from token
        const user = parseJwt(token);
        currentUser = {
            id: user.sub,
            username: user.username,
            role: user.role
        };

        // Update UI for logged in user
        $('#authButtons').hide();
        $('#userProfile').show();
        $('#username').text(currentUser.username);

        // Show role specific elements
        $(`.role-${currentUser.role}`).show();

        // Setup profile dropdown
        setupProfileDropdown();
    } else {
        // Update UI for guest
        $('#authButtons').show();
        $('#userProfile').hide();
        $('.role-specific').hide();
    }

    // Cập nhật badge giỏ hàng
    updateCartBadge();
}

// Load products on homepage
function loadProducts(search = null, category = null, sortBy = null) {
    let url = `${API_URL}/products?limit=12`;

    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }

    if (category) {
        url += `&category=${encodeURIComponent(category)}`;
    }

    if (sortBy) {
        url += `&sort_by=${encodeURIComponent(sortBy)}`;
    }

    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            // Phân chia sản phẩm theo các danh mục hiển thị
            const flashSaleProducts = response.slice(0, 4);
            const featuredProducts = response.slice(4, 8);
            const superDealProducts = response.slice(8, 12);
            const suggestedProducts = response.slice(0, 4); // Dùng lại 4 sản phẩm đầu cho mục đề xuất

            // Hiển thị các sản phẩm vào các container tương ứng
            renderProductsByType('#flashSaleProducts', flashSaleProducts);
            renderProductsByType('#featuredProducts', featuredProducts);
            renderProductsByType('#superDealProducts', superDealProducts);
            renderProductsByType('#suggestedProducts', suggestedProducts);

            // Cập nhật countdown cho flash sale
            updateFlashSaleCountdown();
        },
        error: function(error) {
            showAlert('Không thể tải sản phẩm. Vui lòng thử lại sau.', 'danger');
            console.error(error);
        }
    });
}

// Hàm hiển thị sản phẩm theo từng loại
function renderProductsByType(containerId, products) {
    const container = $(containerId);
    if (!container.length) return;

    container.empty();

    if (products.length === 0) {
        container.html('<div class="empty-products">Không có sản phẩm</div>');
        return;
    }

    products.forEach(product => {
        // Tính phần trăm giảm giá
        const discount = product.original_price ?
            Math.round((1 - product.price / product.original_price) * 100) : 0;

        const productCard = `
            <div class="product-card" data-id="${product._id}">
                ${discount > 0 ? `<div class="discount-tag">-${discount}%</div>` : ''}
                <div class="product-image">
                    <img src="${product.images?.[0] || 'https://via.placeholder.com/150x150?text=No+Image'}" alt="${product.name}">
                </div>
                <div class="product-info">
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">
                        ₫${formatCurrency(product.price)}
                        ${product.original_price ? `<span class="original-price">₫${formatCurrency(product.original_price)}</span>` : ''}
                    </div>
                </div>
            </div>
        `;

        container.append(productCard);
    });

    // Thêm sự kiện click cho các sản phẩm
    $(`${containerId} .product-card`).on('click', function() {
        const productId = $(this).data('id');
        window.location.href = `/product_detail.html?id=${productId}`;
    });
}

// Hàm cập nhật countdown cho flash sale
function updateFlashSaleCountdown() {
    // Giả lập thời gian kết thúc Flash Sale (6 tiếng từ thời điểm hiện tại)
    const now = new Date();
    const endTime = new Date(now);
    endTime.setHours(endTime.getHours() + 6);

    // Cập nhật countdown
    function updateTimer() {
        const now = new Date();
        const diff = endTime - now;

        if (diff <= 0) {
            // Kết thúc Flash Sale, reset thời gian
            const newEndTime = new Date();
            newEndTime.setHours(newEndTime.getHours() + 6);
            endTime = newEndTime;
        }

        // Tính toán giờ, phút, giây
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Cập nhật hiển thị
        $('#hours').text(hours.toString().padStart(2, '0'));
        $('#minutes').text(minutes.toString().padStart(2, '0'));
        $('#seconds').text(seconds.toString().padStart(2, '0'));
    }

    // Gọi hàm lần đầu và thiết lập interval
    updateTimer();
    setInterval(updateTimer, 1000);
}

// Load product detail page
function loadProductDetail() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (!productId) {
        window.location.href = 'index.html';
        return;
    }
    
    $.ajax({
        url: `${API_URL}/products/${productId}`,
        type: 'GET',
        success: function(product) {
            // Update product details
            $('#productTitle').text(product.name);
            $('#productPrice').text(formatCurrency(product.price));
            $('#productLocation').text(product.location);
            $('#productCategory').text(product.category);
            $('#productDescription').text(product.description);
            $('#productStock').text(product.stock);
            
            // Setup add to cart button
            $('#addToCartBtn').attr('data-id', product._id);
            $('#addToCartBtn').attr('data-name', product.name);
            $('#addToCartBtn').attr('data-price', product.price);
            
            // Load product image
            if (product.images && product.images.length > 0) {
                $('#productImage').attr('src', product.images[0]);
            } else {
                $('#productImage').attr('src', 'https://via.placeholder.com/600x400');
            }
            
            // Load reviews
            loadProductReviews(productId);
        },
        error: function(error) {
            showAlert('Không thể tải thông tin sản phẩm. Vui lòng thử lại sau.', 'danger');
            console.error(error);
        }
    });
}

// Load product reviews
function loadProductReviews(productId) {
    $.ajax({
        url: `${API_URL}/products/${productId}/reviews`,
        type: 'GET',
        success: function(reviews) {
            const reviewsContainer = $('#reviewsContainer');
            reviewsContainer.empty();
            
            if (reviews.length === 0) {
                reviewsContainer.html('<p class="text-muted">Chưa có đánh giá nào cho sản phẩm này.</p>');
                return;
            }
            
            reviews.forEach(review => {
                const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
                const reviewItem = `
                    <div class="mb-3 p-3 border rounded">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <div class="text-warning">${stars}</div>
                            <small class="text-muted">${new Date(review.created_at).toLocaleDateString()}</small>
                        </div>
                        <p class="mb-0">${review.comment}</p>
                    </div>
                `;
                reviewsContainer.append(reviewItem);
            });
        },
        error: function(error) {
            console.error(error);
        }
    });
}

// Load cart page
function loadCart() {
    const cart = getCart();
    const cartItemsContainer = $('#cartItems');
    const cartSummaryContainer = $('#cartSummary');
    
    cartItemsContainer.empty();
    
    if (cart.items.length === 0) {
        cartItemsContainer.html('<div class="text-center py-5"><h3>Giỏ hàng trống</h3><p>Hãy thêm sản phẩm vào giỏ hàng</p><a href="index.html" class="btn btn-primary">Tiếp tục mua sắm</a></div>');
        cartSummaryContainer.hide();
        return;
    }
    
    let total = 0;
    
    cart.items.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        const cartItem = `
            <div class="cart-item d-flex align-items-center">
                <div class="flex-shrink-0">
                    <img src="https://via.placeholder.com/100" alt="${item.name}" width="100" class="rounded">
                </div>
                <div class="flex-grow-1 ms-3">
                    <h5>${item.name}</h5>
                    <p class="text-primary mb-1">${formatCurrency(item.price)}</p>
                    <div class="d-flex align-items-center">
                        <div class="input-group input-group-sm" style="width: 120px">
                            <button class="btn btn-outline-secondary" type="button" onclick="updateCartQuantity('${item.id}', ${Math.max(1, item.quantity - 1)})">-</button>
                            <input type="number" class="form-control text-center cart-quantity" value="${item.quantity}" min="1" data-id="${item.id}">
                            <button class="btn btn-outline-secondary" type="button" onclick="updateCartQuantity('${item.id}', ${item.quantity + 1})">+</button>
                        </div>
                        <button class="btn btn-sm btn-link text-danger ms-3 remove-from-cart" data-id="${item.id}">
                            <i class="bi bi-trash"></i> Xóa
                        </button>
                    </div>
                </div>
                <div class="ms-auto text-end">
                    <strong>${formatCurrency(itemTotal)}</strong>
                </div>
            </div>
        `;
        
        cartItemsContainer.append(cartItem);
    });
    
    // Update cart summary
    cartSummaryContainer.show();
    $('#subtotal').text(formatCurrency(total));
    $('#shipping').text(formatCurrency(30000)); // Fixed shipping cost
    $('#total').text(formatCurrency(total + 30000));
}

// Load seller dashboard
function loadSellerDashboard() {
    if (!currentUser || (currentUser.role !== 'seller' && currentUser.role !== 'admin')) {
        window.location.href = 'index.html';
        return;
    }
    
    // Get seller stats
    $.ajax({
        url: `${API_URL}/seller/dashboard`,
        type: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        success: function(response) {
            // Update dashboard stats
            $('#totalProducts').text(response.counts.total_products);
            $('#totalOrders').text(response.counts.total_orders);
            $('#totalRevenue').text(formatCurrency(response.counts.total_revenue));
            
            // Render recent orders
            const ordersContainer = $('#recentOrders');
            ordersContainer.empty();
            
            if (response.recent_orders.length === 0) {
                ordersContainer.html('<tr><td colspan="5" class="text-center">Không có đơn hàng nào gần đây</td></tr>');
            } else {
                response.recent_orders.forEach(order => {
                    const orderRow = `
                        <tr>
                            <td>${order._id.substr(0, 8)}...</td>
                            <td>${formatDate(order.created_at)}</td>
                            <td>${formatCurrency(order.total)}</td>
                            <td><span class="badge bg-${getStatusColor(order.status)}">${getStatusText(order.status)}</span></td>
                            <td><a href="#" class="btn btn-sm btn-outline-primary view-order" data-id="${order._id}">Chi tiết</a></td>
                        </tr>
                    `;
                    ordersContainer.append(orderRow);
                });
            }
            
            // Render stock alerts
            const alertsContainer = $('#stockAlerts');
            alertsContainer.empty();
            
            if (response.stock_alerts.length === 0) {
                alertsContainer.html('<tr><td colspan="4" class="text-center">Không có cảnh báo tồn kho nào</td></tr>');
            } else {
                response.stock_alerts.forEach(product => {
                    const alertRow = `
                        <tr>
                            <td>${product.name}</td>
                            <td>${product.category}</td>
                            <td><span class="badge bg-warning">${product.stock}</span></td>
                            <td><a href="#" class="btn btn-sm btn-outline-primary update-stock" data-id="${product._id}">Cập nhật</a></td>
                        </tr>
                    `;
                    alertsContainer.append(alertRow);
                });
            }
            
            // Load seller products
            loadSellerProducts();
        },
        error: function(error) {
            showAlert('Không thể tải thông tin dashboard. Vui lòng thử lại sau.', 'danger');
            console.error(error);
        }
    });
}

// Load seller products
function loadSellerProducts() {
    $.ajax({
        url: `${API_URL}/products/seller/me`,
        type: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        success: function(products) {
            const productsContainer = $('#sellerProducts');
            productsContainer.empty();
            
            if (products.length === 0) {
                productsContainer.html('<tr><td colspan="6" class="text-center">Bạn chưa có sản phẩm nào</td></tr>');
                return;
            }
            
            products.forEach(product => {
                const productRow = `
                    <tr>
                        <td>${product.name}</td>
                        <td>${product.category}</td>
                        <td>${formatCurrency(product.price)}</td>
                        <td>${product.stock}</td>
                        <td><span class="badge bg-${product.stock > 0 ? 'success' : 'danger'}">${product.stock > 0 ? 'Còn hàng' : 'Hết hàng'}</span></td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <a href="product_detail.html?id=${product._id}" class="btn btn-outline-primary">Xem</a>
                                <button class="btn btn-outline-secondary edit-product" data-id="${product._id}">Sửa</button>
                                <button class="btn btn-outline-danger delete-product" data-id="${product._id}">Xóa</button>
                            </div>
                        </td>
                    </tr>
                `;
                productsContainer.append(productRow);
            });
        },
        error: function(error) {
            showAlert('Không thể tải danh sách sản phẩm. Vui lòng thử lại sau.', 'danger');
            console.error(error);
        }
    });
}

// Load admin dashboard
function loadAdminDashboard() {
    if (!currentUser || currentUser.role !== 'admin') {
        window.location.href = 'index.html';
        return;
    }
    
    // Get admin stats
    $.ajax({
        url: `${API_URL}/admin/dashboard`,
        type: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        success: function(response) {
            // Update dashboard stats
            $('#totalUsers').text(response.counts.total_users);
            $('#totalProducts').text(response.counts.total_products);
            $('#totalOrders').text(response.counts.total_orders);
            $('#totalReports').text(response.counts.total_reports);
            
            // Render recent users
            const usersContainer = $('#recentUsers');
            usersContainer.empty();
            
            if (response.recent_users.length === 0) {
                usersContainer.html('<tr><td colspan="5" class="text-center">Không có người dùng nào gần đây</td></tr>');
            } else {
                response.recent_users.forEach(user => {
                    const userRow = `
                        <tr>
                            <td>${user.username}</td>
                            <td>${user.email}</td>
                            <td>${formatDate(user.created_at)}</td>
                            <td><span class="badge bg-${getRoleBadge(user.role)}">${user.role}</span></td>
                            <td>
                                <div class="btn-group btn-group-sm">
                                    <button class="btn btn-outline-secondary edit-user" data-id="${user._id}">Sửa</button>
                                    <button class="btn btn-outline-danger delete-user" data-id="${user._id}">Xóa</button>
                                </div>
                            </td>
                        </tr>
                    `;
                    usersContainer.append(userRow);
                });
            }
            
            // Render recent orders
            const ordersContainer = $('#recentOrders');
            ordersContainer.empty();
            
            if (response.recent_orders.length === 0) {
                ordersContainer.html('<tr><td colspan="5" class="text-center">Không có đơn hàng nào gần đây</td></tr>');
            } else {
                response.recent_orders.forEach(order => {
                    const orderRow = `
                        <tr>
                            <td>${order._id.substr(0, 8)}...</td>
                            <td>${formatDate(order.created_at)}</td>
                            <td>${formatCurrency(order.total)}</td>                            
                            <td><span class="badge bg-${getStatusColor(order.status)}">${getStatusText(order.status)}</span></td>
                            <td><a href="#" class="btn btn-sm btn-outline-primary view-order" data-id="${order._id}">Chi tiết</a></td>
                        </tr>
                    `;
                    ordersContainer.append(orderRow);
                });
            }
            
            // Render pending reports
            const reportsContainer = $('#pendingReports');
            reportsContainer.empty();
            
            if (response.pending_reports.length === 0) {
                reportsContainer.html('<tr><td colspan="5" class="text-center">Không có báo cáo nào đang chờ xử lý</td></tr>');
            } else {
                response.pending_reports.forEach(report => {
                    const reportRow = `
                        <tr>
                            <td>${report.product_id.substr(0, 8)}...</td>
                            <td>${report.reason}</td>
                            <td>${formatDate(report.created_at)}</td>
                            <td>
                                <div class="btn-group btn-group-sm">
                                    <button class="btn btn-outline-success approve-report" data-id="${report._id}">Chấp nhận</button>
                                    <button class="btn btn-outline-danger reject-report" data-id="${report._id}">Từ chối</button>
                                </div>
                            </td>
                        </tr>
                    `;
                    reportsContainer.append(reportRow);
                });
            }
        },
        error: function(error) {
            showAlert('Không thể tải thông tin dashboard. Vui lòng thử lại sau.', 'danger');
            console.error(error);
        }
    });
}

// Authentication functions
function login() {
    const email = $('#loginEmail').val();
    const password = $('#loginPassword').val();
    
    $.ajax({
        url: `${API_URL}/auth/login`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            email: email,
            password: password
        }),
        success: function(response) {
            // Store token
            localStorage.setItem('token', response.access_token);
            
            // Show success message
            showAlert('Đăng nhập thành công!', 'success');
            
            // Redirect
            const urlParams = new URLSearchParams(window.location.search);
            const redirect = urlParams.get('redirect') || 'index.html';
            setTimeout(() => {
                window.location.href = redirect;
            }, 1000);
        },
        error: function(error) {
            let message = 'Đăng nhập thất bại!';
            if (error.responseJSON && error.responseJSON.detail) {
                message = error.responseJSON.detail;
            }
            showAlert(message, 'danger');
        }
    });
}

function register() {
    const username = $('#registerUsername').val();
    const email = $('#registerEmail').val();
    const password = $('#registerPassword').val();
    const role = $('#registerRole').val();
    
    $.ajax({
        url: `${API_URL}/auth/register`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            username: username,
            email: email,
            password: password,
            role: role
        }),
        success: function(response) {
            // Store token
            localStorage.setItem('token', response.access_token);
            
            // Show success message
            showAlert('Đăng ký thành công!', 'success');
            
            // Redirect
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);
        },
        error: function(error) {
            let message = 'Đăng ký thất bại!';
            if (error.responseJSON && error.responseJSON.detail) {
                message = error.responseJSON.detail;
            }
            showAlert(message, 'danger');
        }
    });
}

function logout() {
    // Clear token and user data
    localStorage.removeItem('token');
    currentUser = null;
    
    // Show success message
    showAlert('Đã đăng xuất thành công!', 'success');
    
    // Redirect to home
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// Cart functions
function getCart() {
    const cartJson = localStorage.getItem('cart');
    if (cartJson) {
        return JSON.parse(cartJson);
    }
    return { items: [] };
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
}

function updateCartBadge() {
    const cart = getCart();
    const itemCount = cart.items.reduce((total, item) => total + item.quantity, 0);
    $('.cart-badge').text(itemCount);
}

function addToCart(productId, productName, productPrice) {
    if (!currentUser) {
        window.location.href = 'login.html?redirect=product_detail.html?id=' + productId;
        return;
    }
    
    const cart = getCart();
    const existingItem = cart.items.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.items.push({
            id: productId,
            name: productName,
            price: productPrice,
            quantity: 1
        });
    }
    
    saveCart(cart);
    showAlert('Đã thêm sản phẩm vào giỏ hàng!', 'success');
}

function updateCartItemQuantity(productId, quantity) {
    const cart = getCart();
    const itemIndex = cart.items.findIndex(item => item.id === productId);
    
    if (itemIndex !== -1) {
        if (quantity <= 0) {
            cart.items.splice(itemIndex, 1);
        } else {
            cart.items[itemIndex].quantity = quantity;
        }
        
        saveCart(cart);
        loadCart();
    }
}

function updateCartQuantity(productId, quantity) {
    updateCartItemQuantity(productId, quantity);
}

function removeFromCart(productId) {
    const cart = getCart();
    cart.items = cart.items.filter(item => item.id !== productId);
    saveCart(cart);
    loadCart();
    showAlert('Đã xóa sản phẩm khỏi giỏ hàng!', 'success');
}

function checkout() {
    if (!currentUser) {
        window.location.href = 'login.html?redirect=cart.html';
        return;
    }
    
    const cart = getCart();
    
    if (cart.items.length === 0) {
        showAlert('Giỏ hàng trống!', 'warning');
        return;
    }
    
    const shippingAddress = $('#shippingAddress').val();
    const phoneNumber = $('#phoneNumber').val();
    
    if (!shippingAddress || !phoneNumber) {
        showAlert('Vui lòng nhập địa chỉ giao hàng và số điện thoại!', 'warning');
        return;
    }
    
    // Calculate total
    const total = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0) + 30000;
    
    // Prepare order data
    const orderData = {
        items: cart.items.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price,
            name: item.name
        })),
        total: total,
        shipping_address: shippingAddress,
        phone_number: phoneNumber
    };
    
    // Send order to server
    $.ajax({
        url: `${API_URL}/orders`,
        type: 'POST',
        contentType: 'application/json',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        data: JSON.stringify(orderData),
        success: function(response) {
            // Clear cart
            localStorage.removeItem('cart');
            updateCartBadge();
            
            // Show success message
            showAlert('Đặt hàng thành công!', 'success');
            
            // Redirect to homepage
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        },
        error: function(error) {
            let message = 'Đặt hàng thất bại!';
            if (error.responseJSON && error.responseJSON.detail) {
                message = error.responseJSON.detail;
            }
            showAlert(message, 'danger');
        }
    });
}

// Helper functions
function showAlert(message, type) {
    const alertDiv = $(`<div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`);
    
    $('#alertContainer').append(alertDiv);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.alert('close');
    }, 5000);
}

function formatCurrency(amount) {
    // Đối với số tiền số nguyên, ta có thể dùng cách đơn giản
    return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

function getStatusColor(status) {
    switch (status) {
        case 'pending': return 'warning';
        case 'processing': return 'primary';
        case 'shipped': return 'info';
        case 'delivered': return 'success';
        case 'cancelled': return 'danger';
        default: return 'secondary';
    }
}

function getStatusText(status) {
    switch (status) {
        case 'pending': return 'Chờ xử lý';
        case 'processing': return 'Đang xử lý';
        case 'shipped': return 'Đang vận chuyển';
        case 'delivered': return 'Đã giao hàng';
        case 'cancelled': return 'Đã hủy';
        default: return status;
    }
}

function getRoleBadge(role) {
    switch (role) {
        case 'admin': return 'danger';
        case 'seller': return 'success';
        case 'user': return 'primary';
        default: return 'secondary';
    }
}

function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Sự kiện khi trang đã tải xong
$(document).ready(function() {
    // Nếu user đã đăng nhập, load profile
    if (currentUser) {
        // Load thông tin profile từ API (mock)
        $('#profileName').val(currentUser.username);
    }
});