select "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" from "django_session" where ("django_session"."expire_date" > '2
024-09-03 11:53:58.438583' and "django_session"."session_key" = 'inlu9kbkg1ge3zxbiqb38qwo0vup9v4d') LIMIT 21; args=('2024-09-03 11:53:58.438583', 'inlu9kbkg1ge3zxbiqb38qwo0vup9v4d'); alias=default

select "users_user"."id", "users_user"."password", "users_user"."last_login", "users_user"."email", "users_user"."first_name", "users_user"."last_name", "users_user"."is_active", "users_user"."is_staff", "users_user"."is_superuser", "users_user"."role_id" from "users_user" where "users_user"."id" = 1 LIMIT 21; args=(1,); alias=default

select "products_category"."id", "products_category"."name", "products_category"."slug", "products_category"."description", "products_category"."icon", "products_categ
ory"."archived", "products_category"."parent_id", "products_category"."lft", "products_category"."rght", "products_category"."tree_id", "products_category"."level" from "products_category" order by "products_category"."name" asc, "products_category"."id" asc; args=(); alias=default

select "products_seller"."id", "products_seller"."name", "products_seller"."slug", "products_seller"."description", "products_seller"."email", "products_seller"."phone", "products_seller"."address", "products_seller"."image" from "products_seller"; args=(); alias=default

select count(*) as "__count" from "products_product"; args=(); alias=default

select count(*) as "__count" from "products_product"; args=(); alias=default



select
    "products_product"."id",
    "products_product"."name",
    "products_product"."slug",
    "products_product"."description",
    "products_product"."archived",
    "products_product"."category_id",
    "products_category"."id",
    "products_category"."name",
    "products_category"."slug",
    "products_category"."description",
    "products_category"."icon",
    "products_category"."archived",
    "products_category"."parent_id",
    "products_category"."lft",
    "products_category"."rght",
    "products_category"."tree_id",
    "products_category"."level" from
    "products_product" inner join "products_category" on (
    "products_product"."category_id" = "products_category"."id")
    order by "products_product"."name" asc, "products_product"."id" asc; args=(); alias=default

select (
    "products_discount_products"."product_id") as "_prefetch_related_val_product_id",
    "products_discount"."id",
    "products_discount"."action_scheme",
    "products_discount"."percent",
    "products_discount"."description",
    "products_discount"."from_date",
    "products_discount"."to_date",
    "products_discount"."is_active",
    "products_discount"."archived" from "products_discount"
inner join "products_discount_products" on (
"products_discount"."id" = "products_discount_products"."discount_id")
where "products_discount_products"."product_id" in (7, 4, 6, 5, 1, 3, 2)
order by "products_discount"."to_date" desc; args=(7, 4, 6, 5, 1, 3, 2); alias=default

select
    "products_sellerprice"."id",
    "products_sellerprice"."product_id",
    "products_sellerprice"."seller_id",
    "products_sellerprice"."price",
    "products_sellerprice"."is_limited",
    "products_sellerprice"."count_products",
    "products_sellerprice"."archived",
    "products_sellerprice"."created_at"
from "products_sellerprice"
where "products_sellerprice"."product_id" in (7, 4, 6, 5, 1, 3, 2); args=(7, 4, 6, 5, 1, 3, 2); alias=default

select
    "products_sellerprice"."id",
    "products_sellerprice"."product_id",
    "products_sellerprice"."seller_id",
    "products_sellerprice"."price",
    "products_sellerprice"."is_limited",
    "products_sellerprice"."count_products",
    "products_sellerprice"."archived",
    "products_sellerprice"."created_at"
from "products_sellerprice"
where ("products_sellerprice"."product_id" = 7 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(7, 0); alias=default

select
    "products_discount"."id",
    "products_discount"."action_scheme",
    "products_discount"."percent",
    "products_discount"."description",
    "products_discount"."from_date",
    "products_discount"."to_date",
    "products_discount"."is_active",
    "products_discount"."archived"
from "products_discount"
inner join "products_discount_products" on ("products
_discount"."id" = "products_discount_products"."discount_id")
where ("products_discount_products"."product_id" = 7 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(7,); alias=default

select
    "products_sellerprice"."id",
    "products_sellerprice"."product_id",
    "products_sellerprice"."seller_id",
    "products_sellerprice"."price",
    "products_sellerprice"."is_limited",
    "products_sellerprice"."count_products",
    "products_sellerprice"."archived",
    "products_sellerprice"."created_at"
from "products_sellerprice"
where ("products_sellerprice"."product_id" = 7 and not "products_sellerprice"."archived"); args=(7,); alias=default

select
    "products_sellerprice"."id",
    "products_sellerprice"."product_id",
    "products_sellerprice"."seller_id",
    "products_sellerprice"."price",
    "products_sellerprice"."is_limited",
    "products_sellerprice"."count_products",
    "products_sellerprice"."archived",
    "products_sellerprice"."created_at"
from "products_sellerprice"
where ("products_sellerprice"."product_id" = 4 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(4, 0); alias=default

select
    "products_discount"."id",
    "products_discount"."action_scheme",
    "products_discount"."percent",
    "products_discount"."description", "
    products_discount"."from_date",
    "products_discount"."to_date",
    "products_discount"."is_active",
    "products_discount"."archived"
from "products_discount" inner join "products_discount_products" on
("products_discount"."id" = "products_discount_products"."discount_id")
where ("products_discount_products"."product_id" = 4 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(4,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 4 and not "products_sellerprice"."archived"); args=(4,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 6 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(6, 0); alias=default

select "products_discount"."id", "products_discount"."action_scheme", "products_discount"."percent", "products_discount"."description", "products_discount"."from_date"
, "products_discount"."to_date", "products_discount"."is_active", "products_discount"."archived" from "products_discount" inner join "products_discount_products" on ("products
_discount"."id" = "products_discount_products"."discount_id") where ("products_discount_products"."product_id" = 6 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(6,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 6 and not "products_sellerprice"."archived"); args=(6,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 5 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(5, 0); alias=default

select "products_discount"."id", "products_discount"."action_scheme", "products_discount"."percent", "products_discount"."description", "products_discount"."from_date"
, "products_discount"."to_date", "products_discount"."is_active", "products_discount"."archived" from "products_discount" inner join "products_discount_products" on ("products
_discount"."id" = "products_discount_products"."discount_id") where ("products_discount_products"."product_id" = 5 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(5,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 5 and not "products_sellerprice"."archived"); args=(5,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 1 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(1, 0); alias=default

select "products_discount"."id", "products_discount"."action_scheme", "products_discount"."percent", "products_discount"."description", "products_discount"."from_date"
, "products_discount"."to_date", "products_discount"."is_active", "products_discount"."archived" from "products_discount" inner join "products_discount_products" on ("products
_discount"."id" = "products_discount_products"."discount_id") where ("products_discount_products"."product_id" = 1 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(1,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 1 and not "products_sellerprice"."archived"); args=(1,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 3 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(3, 0); alias=default

select "products_discount"."id", "products_discount"."action_scheme", "products_discount"."percent", "products_discount"."description", "products_discount"."from_date"
, "products_discount"."to_date", "products_discount"."is_active", "products_discount"."archived" from "products_discount" inner join "products_discount_products" on ("products
_discount"."id" = "products_discount_products"."discount_id") where ("products_discount_products"."product_id" = 3 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(3,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 3 and not "products_sellerprice"."archived"); args=(3,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 2 and not "products_sellerprice"."archived" and "products_sellerprice"."count_products" > 0); args=(2, 0); alias=default

select "products_discount"."id", "products_discount"."action_scheme", "products_discount"."percent", "products_discount"."description", "products_discount"."from_date"
, "products_discount"."to_date", "products_discount"."is_active", "products_discount"."archived" from "products_discount" inner join "products_discount_products" on ("products
_discount"."id" = "products_discount_products"."discount_id") where ("products_discount_products"."product_id" = 2 and not "products_discount"."archived" and "products_discount"."is_active") order by "products_discount"."to_date" desc; args=(2,); alias=default

select "products_sellerprice"."id", "products_sellerprice"."product_id", "products_sellerprice"."seller_id", "products_sellerprice"."price", "products_sellerprice"."is
_limited", "products_sellerprice"."count_products", "products_sellerprice"."archived", "products_sellerprice"."created_at" from "products_sellerprice" where ("products_sellerprice"."product_id" = 2 and not "products_sellerprice"."archived"); args=(2,); alias=default

select "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" from "django_session" where ("django_session"."expire_date" > '2
024-09-03 11:53:58.521583' and "django_session"."session_key" = 'inlu9kbkg1ge3zxbiqb38qwo0vup9v4d') LIMIT 21; args=('2024-09-03 11:53:58.521583', 'inlu9kbkg1ge3zxbiqb38qwo0vup9v4d'); alias=default

select "users_user"."id", "users_user"."password", "users_user"."last_login", "users_user"."email", "users_user"."first_name", "users_user"."last_name", "users_user"."is_active", "users_user"."is_staff", "users_user"."is_superuser", "users_user"."role_id" from "users_user" where "users_user"."id" = 1 LIMIT 21; args=(1,); alias=default