using System;
using System.Threading;

public class Game
{
	public int CurrentNumber;
	string UserInput;

	static bool CheckAnswer(int currentNumber, string userInput)
    {
		bool isFizz = currentNumber % 2 == 0;
		bool isBuzz = currentNumber % 3 == 0;
		bool isBazz = currentNumber % 5 == 0;

		if (isFizz && !userInput.Contains("fizz"))
        {
			return false;
        } else if (isBuzz && !userInput.Contains("buzz"))
        {
			return false;
        } else if (isBazz && !userInput.Contains("bazz"))
        {
			return false;
        } else
        {
			return true;
        }
	}

	public void Start()
    {
		while (true)
        {

			Console.WriteLine("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
			Console.Write($"Current number: {CurrentNumber}. \nType your answer: ");

			UserInput = Console.ReadLine().ToLower();

			if (!CheckAnswer(CurrentNumber, UserInput))
            {
				Console.WriteLine("Wrong.");
				Thread.Sleep(1000);
				break;
            } else
            {
				CurrentNumber++;
				Console.WriteLine("Correct!");
				Thread.Sleep(1000);
            }
		}
	}

	public Game(Player player)
	{
		player.Score = 0;
		CurrentNumber = 1;
	}
}
