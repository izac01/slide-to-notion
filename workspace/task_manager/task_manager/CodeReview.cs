using System;
using System.Collections.Generic;
using SharpDiff;
using Octokit;

// CodeReview class
public class CodeReview
{
    private List<Code> codes;
    private GitHubClient client;

    public CodeReview()
    {
        this.codes = new List<Code>();
        this.client = new GitHubClient(new ProductHeaderValue("MyApp"));
    }

    public async void SubmitCode(Code code, User user)
    {
        if (code == null)
        {
            throw new ArgumentNullException(nameof(code));
        }

        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        // Add the code to the list of codes
        this.codes.Add(code);

        // Integrate with GitHub API using Octokit for code submission
        var createFileRequest = new CreateFileRequest("Initial commit", code.GetContent());
        await client.Repository.Content.CreateFile("owner", "repo", "path", createFileRequest);
    }

    public void ReviewCode(Code code, User user)
    {
        if (code == null)
        {
            throw new ArgumentNullException(nameof(code));
        }

        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        // Integrate with SharpDiff for diff generation
        var existingCode = this.codes.FindLast(c => c.GetSubmitter().GetName() == user.GetName());
        if (existingCode != null)
        {
            var diff = SharpDiff.Compare(existingCode.GetContent(), code.GetContent());
            foreach (var line in diff.Lines)
            {
                Console.WriteLine(line);
            }
        }
    }
}
