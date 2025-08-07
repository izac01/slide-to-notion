using System;

// NotificationSystem class
public class NotificationSystem
{
    public void SendNotification(User user, string message)
    {
        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        if (string.IsNullOrEmpty(message))
        {
            throw new ArgumentException("Message cannot be null or empty", nameof(message));
        }

        // In a real-world application, this would likely involve sending an email, SMS, or other type of notification.
        // For this example, we'll just write the notification to the console.
        Console.WriteLine($"Notification for {user.GetName()}: {message}");
    }
}
