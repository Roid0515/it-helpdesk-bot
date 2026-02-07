-- helpdesk_db 테이블 생성 (MariaDB 12.1.x / models.py 구조와 동일)
-- DBeaver에서 helpdesk_db 연결 선택 후, 아래 두 개의 CREATE TABLE을 각각 선택해서 실행하세요.

-- ========== 1) 아래 블록만 선택 후 실행 (Ctrl+Enter) ==========
CREATE TABLE IF NOT EXISTS `helpdesk_requests` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(100) NOT NULL,
  `user_department` VARCHAR(100) DEFAULT NULL,
  `user_contact` VARCHAR(100) DEFAULT NULL,
  `title` VARCHAR(200) NOT NULL,
  `content` TEXT NOT NULL,
  `category` VARCHAR(50) DEFAULT NULL,
  `status` VARCHAR(20) DEFAULT 'pending',
  `created_at` DATETIME DEFAULT NULL,
  `request_date` DATE DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== 2) 아래 블록만 선택 후 실행 (Ctrl+Enter) ==========
CREATE TABLE IF NOT EXISTS `daily_inboxes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `inbox_date` DATE NOT NULL,
  `created_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inbox_date` (`inbox_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
