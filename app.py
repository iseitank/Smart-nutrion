import streamlit as st
import requests

# ---------------- פונקציה לשליפת נתוני מזון ----------------
def search_food(query):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    data = response.json()
    results = data.get("products", [])
    if results:
        product = results[0]
        nutrients = product.get("nutriments", {})
        return {
            "name": product.get("product_name", "לא ידוע"),
            "calories": nutrients.get("energy-kcal_100g", 0),
            "protein": nutrients.get("proteins_100g", 0),
            "carbs": nutrients.get("carbohydrates_100g", 0),
            "fat": nutrients.get("fat_100g", 0),
        }
    else:
        return None

# ---------------- כותרת ----------------
st.set_page_config(page_title="תזונאי חכם", page_icon="🥗", layout="centered")
st.title("תזונאי חכם אישי")
st.write("עקוב אחרי מה שאכלת, בדוק חוסרים, וקבל המלצות חכמות")

# ---------------- מצב גלובלי לאוכל שנאכל ----------------
if "eaten_today" not in st.session_state:
    st.session_state.eaten_today = []

# ---------------- הוספת מאכלים ----------------
st.subheader("מה אכלת היום?")
food_query = st.text_input("שם מאכל")
if st.button("חפש והוסף"):
    if food_query:
        food_data = search_food(food_query)
        if food_data:
            st.session_state.eaten_today.append(food_data)
            st.success(f"{food_data['name']} נוסף!")
        else:
            st.error("לא נמצא מידע על המאכל הזה")

# ---------------- תצוגת סיכום יומי ----------------
if st.session_state.eaten_today:
    st.subheader("סיכום יומי")
    total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    for item in st.session_state.eaten_today:
        st.markdown(f"**{item['name']}**")
        st.write(f"קלוריות: {item['calories']} kcal, חלבון: {item['protein']}g, פחמימות: {item['carbs']}g, שומן: {item['fat']}g")
        for k in total:
            total[k] += item[k]

    st.markdown("---")
    st.markdown("### סיכום תזונתי יומי")
    st.write(f"**סה\"כ קלוריות:** {total['calories']} / 2500")
    st.write(f"**חלבון:** {total['protein']}g / 56g")
    st.write(f"**פחמימות:** {total['carbs']}g / 300g")
    st.write(f"**שומן:** {total['fat']}g / 70g")

# ---------------- קלט בדיקות דם ----------------
st.markdown("---")
st.subheader("הכנס ערכים מבדיקת דם")
vitamin_d = st.number_input("ויטמין D (ng/mL)", min_value=0.0, max_value=150.0, step=0.1)
b12 = st.number_input("B12 (pg/mL)", min_value=0.0, max_value=2000.0, step=1.0)
iron = st.number_input("ברזל (µg/dL)", min_value=0.0, max_value=300.0, step=1.0)

# ---------------- המלצות אישיות ----------------
st.subheader("המלצות תזונתיות מותאמות")
if vitamin_d < 30:
    st.warning("ויטמין D נמוך — שקול לצרוך סלמון, ביצים או תוסף.")
if b12 < 300:
    st.warning("B12 נמוך — מומלץ לאכול ביצים, דגים, בשר או תוסף.")
if iron < 60:
    st.warning("ברזל נמוך — נסה עדשים, בשר אדום, טופו או תרד.")
if vitamin_d >= 30 and b12 >= 300 and iron >= 60:
    st.success("מעולה! כל הערכים שלך בטווח התקין.")
