import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import {
    getFirestore,
    collection,
    query,
    orderBy,
    limit,
    onSnapshot,
    getDoc,
    doc,
} from "../libraries/firebase-client/firebase-firestore.js";

const FirebaseClientModule = (function () {
    // Initialize Firebase
    let app;
    let db;
    let unsubscribeNotifications;

    const Init = async function () {
        await GetFirebaseConfig();
    };

    const InitEvents = function () {
        OnSnapshotNotifications();
        window.addEventListener("beforeunload", function () {
            if (unsubscribeNotifications) {
                unsubscribeNotifications();
            }
        });
    };

    const GetFirebaseConfig = async function () {
        const url = "/firebase-configure";
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });
        const data = await response.json();
        if (data) {
            app = initializeApp(data.data);
            db = getFirestore(app);
        }
    };

    /**
     * Subscribe to notifications collection and display the latest 3 notifications
     * Author: TaiPV, created at 2024/05/17
     * @returns {void}
     */
    const OnSnapshotNotifications = function () {
        try {
            const userId = $("#user-id").val();
            if (!userId) return;
            const notifications_ref = collection(
                db,
                "user_notifications",
                userId,
                "notifications"
            );

            // Thực hiện lắng nghe sự thay đổi của collection và hiển thị 3 thông báo mới nhất
            const notification_query = query(
                notifications_ref,
                orderBy("created_at", "desc"),
                limit(3)
            );

            unsubscribeNotifications = onSnapshot(
                notification_query,
                async (snapshot) => {
                    const notifications = snapshot.docs.map((doc) => {
                        return {
                            id: doc.id,
                            ...doc.data(),
                        };
                    });

                    console.log("notifications: ", notifications);
                    if (notifications.length === 0) return;

                    const notificationDropDown = $(
                        ".btn-notification + .dropdown-menu"
                    );
                    notificationDropDown.empty();

                    const notificationItem = $(
                        ".dropdown-item-template .notification-item"
                    ).clone();

                    const sectionClassDetailUrl = $(
                        "#section-class-detail-url"
                    ).val();

                    let isShowBlink = false;
                    for (const notification of notifications) {
                        const notificationItemClone = notificationItem.clone();

                        // Lấy ra thông tin người gửi
                        const senderRef = notification.from;
                        try {
                            // Đợi 2 promise trên chạy xong
                            const [senderDoc, sectionDoc] = await Promise.all([
                                getDoc(senderRef),
                                getDoc(
                                    doc(
                                        db,
                                        "section_class",
                                        notification.section_class_id
                                    )
                                ),
                            ]);

                            const createdAt = new Date(
                                notification.created_at.seconds * 1000 +
                                    notification.created_at.nanoseconds /
                                        1000000
                            );
                            const sender = senderDoc.data();
                            const href =
                                notification?.status === "reject"
                                    ? "javascript:void(0)"
                                    : sectionClassDetailUrl.replace(
                                          "0",
                                          `${notification.section_class_id}?notification_id=${notification.id}`
                                      );

                            notificationItemClone.attr("href", href);

                            // Tô màu cho thông báo chưa đọc
                            notificationItemClone.css(
                                "background-color",
                                notification.is_seen ? "" : "#fcf0db"
                            );

                            isShowBlink |= !notification.is_seen;

                            notificationItemClone
                                .find(".created-at")
                                .text(CommonModule.GetTimeDiff(createdAt));
                            
                            notificationItemClone
                                .find(".sender-name")
                                .text(sender.display_name);
                            notificationItemClone
                                .find(".message")
                                .text(`${notification.type}`);
                            notificationItemClone
                                .find(".section-class-name")
                                .text(sectionDoc.data().name);
                            notificationItemClone
                                .find(".avatar")
                                .attr("src", sender.picture);
                            notificationDropDown.append(notificationItemClone);
                        } catch (error) {
                            console.error("Error getting sender data:", error);
                        }
                    }

                    if (isShowBlink) {
                        $(".notification-blink").removeClass("dis-none");
                    } else {
                        $(".notification-blink").addClass("dis-none");
                    }
                }
            );
        } catch (error) {
            console.log("subscribeNotifications: ", error);
        }
    };

    return {
        Init: Init,
        InitEvents: InitEvents,
    };
})();

await FirebaseClientModule.Init();
FirebaseClientModule.InitEvents();
