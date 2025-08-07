using System;
using System.Collections.Generic;

// TaskStatus enum
public enum TaskStatus
{
    NotStarted,
    InProgress,
    Completed
}

// Task class
public class Task
{
    private string title;
    private User assignee;
    private DateTime deadline;
    private TaskStatus status;

    public Task(string title, User assignee, DateTime deadline)
    {
        this.title = title;
        this.assignee = assignee;
        this.deadline = deadline;
        this.status = TaskStatus.NotStarted;
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

    public void Assign(User user)
    {
        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        this.assignee = user;
    }

    public TaskStatus GetStatus()
    {
        if (DateTime.Now > this.deadline)
        {
            return TaskStatus.Completed;
        }
        else
        {
            return TaskStatus.InProgress;
        }
    }
}

// TaskManager class
public class TaskManager
{
    private List<Task> tasks;

    public TaskManager()
    {
        this.tasks = new List<Task>();
    }

    public void CreateTask(Task task)
    {
        if (task == null)
        {
            throw new ArgumentNullException(nameof(task));
        }

        this.tasks.Add(task);
    }

    public void AssignTask(Task task, User user)
    {
        if (task == null)
        {
            throw new ArgumentNullException(nameof(task));
        }

        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        task.Assign(user);
    }

    public TaskStatus TrackTask(Task task)
    {
        if (task == null)
        {
            throw new ArgumentNullException(nameof(task));
        }

        return task.GetStatus();
    }
}
