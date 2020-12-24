using System;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Threading.Tasks.Sources;

public class Player
{
	public readonly string Name;
	public int Score;

	public Player(string name)
	{
		Name = name;
	}
}
