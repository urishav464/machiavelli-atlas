# Chapter 2 header and the argument ladder. Italian quotes are copied from ~/.atlas-cache/src/machiavelli/discorsi_1_2.txt.
# The Shalem Hebrew (Solon, p. 12) is the only Shalem wording in this chapter. Pages follow the atlas specification
# (Sparta 9 and 12, Athens 12, Rome 12-13, Florence 9, the wheel 10-11); the in-between ranges are bracketed by those.
H = {'n':2, 'eyebrow':'ספר ראשון, פרק 2 · עמ׳ 8–13', 'title':'סוגי הרפובליקות',
 'full':'"מכמה סוגים הן הרפובליקות, ומאיזה סוג הייתה הרפובליקה הרומית" (תרגום חופשי)',
 'oneline':'שישה סוגי ממשל, שכולם מתקלקלים, ומעגל שעובר ביניהם. הפתרון של מקיאוולי הוא ממשל שיש בו מכולם: נסיך, אצילים ועם. לספרטה נתן אותו אדם אחד, ולרומא נתן אותו המקרה.',
 'intro':'ארבעה סיפורים מהפרק, כולם על המפה. בחרו סיפור כדי ללכת בו צעד אחר צעד.',
 'question':'ספרטה קיבלה את חוקיה מאדם אחד, ורומא "במקרה", מתוך מאבקים. איזו דרך טובה יותר? ואם רומא הגיעה לשלמות דווקא בגלל הפירוד בין העם לסנאט, מה זה אומר על פירנצה, שהמקרים שלה סידרו אותה ואז פירקו אותה?',
 'next':'ממשיך בפרק 3: אילו אירועים הביאו ליצירת הטריבונים.',
 'overviewBounds':[[35.2,9.8],[44.8,24.6]], 'hideOther':True}
LADDER = [
 {'role':['פתיחה',''], 'pg':'עמ׳ 9', 'h':'בידי אחד, או במקרה', 'q':'"da uno solo le leggi, e ad un tratto... alcune le hanno avute a caso, ed in più volte": בידי אחד בלבד, ובבת אחת... ואחרות קיבלו אותם במקרה, בכמה פעמים', 'tr':True, 'at':[0,0]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 9', 'h':'פירנצה: המקרה מסדר, והמקרה מפרק', 'q':'"fu dallo accidente d\'Arezzo, nel dua, riordinata; e da quel di Prato, nel dodici, disordinata": המקרה של ארצו, בשנת שתיים, סידר אותה מחדש, וזה של פראטו, בשנת שתים-עשרה, פירק את סדריה', 'tr':True, 'at':[3,1]},
 {'role':['הבחנה','rule'], 'pg':'עמ׳ 9–10', 'h':'שלושה סוגים, או שישה', 'q':'"sei ragioni governi... buoni in loro medesimi, ma sì facili a corrompersi": שישה סוגי ממשל... שלושה טובים כשלעצמם, אבל קלים כל כך להשחית', 'tr':True, 'at':[0,1]},
 {'role':['הכלל','rule'], 'pg':'עמ׳ 10–11', 'h':'הגלגל', 'q':'"E questo è il cerchio nel quale girando tutte le republiche si sono governate e si governano": וזה המעגל שבו, בסיבוב, נוהלו ומתנהלות כל הרפובליקות', 'tr':True, 'at':[1,2]},
 {'role':['הפתרון','rule'], 'pg':'עמ׳ 11–12', 'h':'ממשל שיש בו מכולם', 'q':'"l\'uno guarda l\'altro, sendo in una medesima città il Principato, gli Ottimati, e il Governo Popolare": כל אחד שומר על השני, כשבאותה עיר יש נסיכות, אצילים וממשל עממי', 'tr':True, 'at':[0,1]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 12', 'h':'ליקורגוס: יותר משמונה מאות שנה', 'q':'"fece uno stato che durò più che ottocento anni": יצר מדינה שהחזיקה יותר משמונה מאות שנה', 'tr':True, 'at':[0,3]},
 {'role':['הניגוד','cave'], 'pg':'עמ׳ 12', 'h':'סולון: רק העם', 'q':'כיוון שהסדיר בה רק את הממשל העממי, גרם לכך שיהיה כה קצר ימים', 'at':[1,0]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 12–13', 'h':'רומא: מה שלא עשה מסדר, עשה המקרה', 'q':'"quello che non aveva fatto uno ordinatore, lo fece il caso": מה שלא עשה מסדר, עשה המקרה', 'tr':True, 'at':[2,1]},
 {'role':['הסיום',''], 'pg':'עמ׳ 12–13', 'h':'השלמות באה מהפירוד', 'q':'"alla quale perfezione venne per la disunione della Plebe e del Senato": ולשלמות הזו הגיעה בגלל הפירוד בין הפלבס לסנאט', 'tr':True, 'at':[2,2]},
]
