using System;
using System.Collections.Generic;

// User class
public class User
{
    private string name;

    public User(string name)
    {
        this.name = name;
    }

    public string GetName()
    {
        return this.name;
    }
}

// Task class
public class Task
{
    private string title;
    private User assignee;
    private DateTime deadline;

    public Task(string title, User assignee, DateTime deadline)
    {
        this.title = title;
        this.assignee = assignee;
        this.deadline = deadline;
    }

    public string GetTitle()
    {
        return this.title;
    }

    public User GetAssignee()
    {
        return this.assignee;
    }

    public DateTime GetDeadline()
    {
        return this.deadline;
    }
}

// Code class
public class Code
{
    private string content;
    private User submitter;

    public Code(string content, User submitter)
    {
        this.content = content;
        this.submitter = submitter;
    }

    public string GetContent()
    {
        return this.content;
    }

    public User GetSubmitter()
    {
        return this.submitter;
    }
}

// Main Program class
public class Program
{
    private TaskManager taskManager;
    private CodeReview codeReview;
    private NotificationSystem notificationSystem;

    public Program()
    {
        this.taskManager = new TaskManager();
        this.codeReview = new CodeReview();
        this.notificationSystem = new NotificationSystem();
    }

    public static void Main(string[] args)
    {
        Program program = new Program();

        // Create a user
        User user = new User("Alex");

        // Create a task
        Task task = new Task("Task 1", user, DateTime.Now.AddDays(7));

        // Create a code
        Code code = new Code("Code 1", user);

        // Use TaskManager to create, assign and track task
        program.taskManager.CreateTask(task);
        program.taskManager.AssignTask(task, user);
        program.taskManager.TrackTask(task);

        // Use CodeReview to submit and review code
        program.codeReview.SubmitCode(code, user);
        program.codeReview.ReviewCode(code, user);

        // Use NotificationSystem to send notification
        program.notificationSystem.SendNotification(user, "Task assigned");
    }
}
