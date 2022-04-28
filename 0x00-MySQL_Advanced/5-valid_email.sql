-- SQL script that creates a trigger that resets the attribute
-- valid_email only when the email has been changed.
CREATE TRIGGER update_email BEFORE UPDATE ON users
FOR EACH ROW
SET NEW.valid_email = IF(NEW.email != OLD.email, 0, OLD.valid_email)
