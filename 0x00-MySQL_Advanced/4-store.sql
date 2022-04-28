-- SQL script that creates a trigger that
-- decreases the quantity of an item after adding a new order.
CREATE TRIGGER ins_dec AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET items.quantity = items.quantity - NEW.number WHERE items.name = NEW.item_name;
