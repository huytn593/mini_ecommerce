<?php
require_once('app/config/database.php');
require_once('app/models/AccountModel.php');

class AccountController {
    private $accountModel;
    private $db;

    public function __construct() {
        // Khởi tạo kết nối database và model
        $this->db = (new Database())->getConnection();
        $this->accountModel = new AccountModel($this->db);
    }

    // Hiển thị form đăng ký
    public function register(){
        include_once 'app/views/account/register.php';
    }

    // Hiển thị form đăng nhập
    public function login() {
        include_once 'app/views/account/login.php';
    }

    // Xử lý lưu đăng ký tài khoản
    public function save(){
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $username = trim($_POST['username'] ?? '');
            $fullName = trim($_POST['fullname'] ?? '');
            $password = trim($_POST['password'] ?? '');
            $confirmPassword = trim($_POST['confirmpassword'] ?? '');

            $errors = [];

            if(empty($username)){
                $errors['username'] = "Vui lòng nhập username!";
            }
            if(empty($fullName)){
                $errors['fullname'] = "Vui lòng nhập full name!";
            }
            if(empty($password)){
                $errors['password'] = "Vui lòng nhập password!";
            }
            if($password !== $confirmPassword){
                $errors['confirmPass'] = "Mật khẩu và xác nhận không khớp!";
            }

            // Kiểm tra xem tài khoản đã tồn tại chưa
            $account = $this->accountModel->getAccountByUsername($username);
            if($account){
                $errors['account'] = "Tài khoản này đã được đăng ký!";
            }
            
            if(count($errors) > 0){
                // Nếu có lỗi thì gửi lại form kèm thông báo lỗi
                include_once 'app/views/account/register.php';
            } else {
                // Mã hóa mật khẩu trước khi lưu
                $hashedPassword = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);
                // Lưu tài khoản với role mặc định là "user"
                $result = $this->accountModel->save($username, $fullName, $hashedPassword, "user");
                if($result){
                    header('Location: /mini_ecommerce/account/login');
                    exit;
                } else {
                    echo "Đăng ký không thành công. Vui lòng thử lại!";
                }
            }
        }
    }

    // Xử lý đăng nhập: kiểm tra thông tin đăng nhập, lưu session chứa username và role
    public function checkLogin(){
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $username = trim($_POST['username'] ?? '');
            $password = trim($_POST['password'] ?? '');

            $account = $this->accountModel->getAccountByUsername($username);
            if ($account) {
                // $account->password là chuỗi đã được hash
                if (password_verify($password, $account->password)) {
                    session_start();
                    // Lưu các thông tin cần thiết vào session
                    $_SESSION['username'] = $account->username;
                    $_SESSION['role'] = $account->role;

                    // Chuyển hướng dựa trên role, ví dụ: nếu là seller chuyển đến trang SellerController
                    if ($account->role === 'seller') {
                        header('Location: /mini_ecommerce/controllers/SellerController.php?action=manageProducts');
                    } else {
                        header('Location: /mini_ecommerce/product');
                    }
                    exit;
                } else {
                    echo "Password không chính xác.";
                }
            } else {
                echo "Không tìm thấy tài khoản.";
            }
        }
    }

    // Xử lý đăng xuất: hủy session và chuyển hướng về trang chủ hoặc đăng nhập
    public function logout(){
        session_start();
        unset($_SESSION['username']);
        unset($_SESSION['role']);
        session_destroy();
        header('Location: /mini_ecommerce/product');
        exit;
    }
}
?>
