using System;
using System.Threading;

namespace FizzBuzzBazz
{
    class Program
    {
        static void Welcome()
        {
            Console.WriteLine("Welcome to \"Interactive FizzBuzzBazz\"! Press any key to continue...");
            Console.ReadLine();
        }

        static void HowTo()
        {
            Console.WriteLine(
                $"\n\nGoal of this game is to observe a sequence of whole numbers starting at 1 that are printed to the screen and for each number to type:" +
                $"\na) \"fizz\", if the number is divisible by 2;" +
                $"\nb) \"buzz\", if the number is divisible by 3;" +
                $"\nc) \"bazz\", if the number is divisible by 5;" +
                $"\nd) nothing, if the number can't be divided by either of the aforementioned numbers." +
                $"\n\nKeep in mind that there are occasions when more than one given condition applies, in such cases you have to combine the answers," +
                $"e.g. for number 6 you'd type \"fizzbuzz\", for number 30 - \"fizzbuzzbazz\", and so on. Quotation marks are not needed.");
        }

        static void Main(string[] args)
        {
            Welcome();

            Console.Write("Enter your name: ");
            Player player = new Player(Console.ReadLine());

            Console.WriteLine($"\nWelcome {player.Name}!");
            Thread.Sleep(1000);

            HowTo();

            Thread.Sleep(1000);
            Console.Write("\nPress enter when you're ready to begin. ");
            Console.ReadLine();

            while (true)
            {
                Game game = new Game(player);
                game.Start();

                Console.Write($"\nGame Over, {player.Name}. Your final score is {game.CurrentNumber - 1}. \nPlay again? (Y/n) ");
                if (Console.ReadLine().ToLower() == "n")
                {
                    Console.WriteLine("\nThank you for playing!");
                    Thread.Sleep(1000);
                    break;
                }
            }
        }
    }
}
