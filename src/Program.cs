// Version 1.2.1 - C# Edition
// Date: 2023/7/7 Friday

using System;
using System.IO;
using System.IO.Enumeration;
using System.Net;

using Microsoft.Win32;

public class Program
{
    static string path = "";
    static bool move = false;
    static bool free = false;
    static void Main(string[] args)
    {
        Console.WriteLine("[***] zBot Installer - by terminite\n\n");


        static void CheckFree(string[] args)
        {
            Console.Write("[*] Select zBot: Free Trial (1) or Pro (2): ");
            string? usefree = Console.ReadLine();
            if (usefree == "1")
            {
                free = true;
                Console.WriteLine("[*] Free Trial Selected");
            }
            DirectorySetup(args);
        }

        static void DirectorySetup(string[] args)
        {
            Console.Write("[*] Select Directory: Default (1) or Custom (2): ");
            string? usedir = Console.ReadLine();

            if (usedir == "1")
            {
                path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Geometry Dash";
                Console.WriteLine("[*] Default Directory Selected");
            } else
            {
                Console.Write("[*] Geometry Dash Directory (with executable): ");
                string? desiredpath = Console.ReadLine();

                if (Directory.Exists(desiredpath))
                {
                    if (File.Exists(desiredpath + "\\GeometryDash.exe"))
                    {
                        Console.WriteLine("[*] Geometry Dash.exe found in directory.");
                    } else
                    {
                        Console.WriteLine("[!] Geometry Dash.exe not found in directory. Please try again.\n");
                        DirectorySetup(args);
                    }
                    path = desiredpath;
                    Console.WriteLine("\n[*] Custom Directory Selected");
                } else
                {
                    Console.WriteLine("[!] The Geometry Dash Directory you entered is not a directory. Please try again.\n");
                    DirectorySetup(args);
                }
            }
            Console.WriteLine("\n[*] Selected Directory: " + path);
            MHCheck(args);
        }

        static void MHCheck(string[] args)
        {
            if (File.Exists(path + "\\hackpro.dll"))
            {
                Console.WriteLine("[*] hackpro.dll found in directory.");
                if (File.Exists(path + "\\hackproldr.dll"))
                {
                    Console.WriteLine("[*] hackproldr.dll found in directory.");
                    Console.WriteLine("[!] Detected Mega Hack v7 install in directory. Please uninstall it.\n");
                    Console.ReadKey();
                    Environment.Exit(0);
                } else
                {
                    Console.WriteLine("[*] Detected Mega Hack v6 install in directory.");
                    move = true;
                    DownloadDLLLoader(args);
                }
            } else
            {
                Console.WriteLine("[*] Mega Hack not found.\n");
                DownloadDLLLoader(args);
            }
        }

        static void DownloadDLLLoader(string[] args)
        {
            string dll1 = "https://github.com/adafcaefc/GDDllLoader/releases/download/v2/GDDLLLoader.dll";
            string dll2 = "https://github.com/adafcaefc/GDDllLoader/releases/download/v2/libExtensions.dll";
            
            Console.WriteLine("[*] Downloading GDDLLLoader.dll...");
            using (var client = new WebClient())
            {
                client.DownloadFile(dll1, path + "\\GDDLLLoader.dll");
            }
            Console.WriteLine("[*] Downloading libExtensions.dll...");
            using (var client = new WebClient())
            {
                client.DownloadFile(dll2, path + "\\libExtensions.dll");
            }
            Console.WriteLine("[*] Downloaded GDDLLLoader.dll and libExtensions.dll\n");
            

            if (Directory.Exists(path + "\\adaf-dll"))
            {
                Console.WriteLine("[*] adaf-dll folder found in directory.\n");
                if (move)
                {
                    File.Move(path + "\\hackpro.dll", path + "\\adaf-dll");
                }
            } else
            {
                Console.WriteLine("[*] adaf-dll folder not found in directory.");
                Console.WriteLine("[*] Creating adaf-dll folder...");
                Directory.CreateDirectory(path + "\\adaf-dll");
                Console.WriteLine("[*] Created adaf-dll folder.\n");
            }

            DownloadZBOT(args);
        }

        static void DownloadZBOT(string[] args)
        {
            string filename = "";
            string url = "";

            if (free)
            {
                filename = "zBot Free Trial.dll";
                url = "https://cdn.discordapp.com/attachments/883131563552960553/1126171868710305862/zBot_Free_Trial.dll";
            } else
            {
                filename = "zBot Pro v2.0.0.dll";
                url = "https://zbot.figmentcoding.me/static/archive/zBot%20v2.0.0.dll";
            }

            Console.WriteLine("[*] Downloading " + filename + "...");

            using (var client = new WebClient())
            {
                client.DownloadFile(url, path + "\\adaf-dll\\" + filename);
            }

            Console.WriteLine("[*] Downloaded " + filename + "\n");
            Console.WriteLine("[*] zBot download complete.");
            if (free)
            {
                Finished(args);
            } else
            {
                CheckKey(args);
            }
        }

        static string GetHWID(string[] args)
        {
            string? hwid = (string?)Registry.GetValue("HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "HwProfileGuid", null);
            return hwid;
        }

        static void CheckKey(string[] args)
        {
            string url = "https://zbot.figmentcoding.me/get-guid/";
            string hwid = GetHWID(args);

            Console.Write("[*] Enter your zBot key: ");
            string? key = Console.ReadLine();

            if (key == "")
            {
                Console.WriteLine("[!] You did not enter a key. Please try again.\n");
                CheckKey(args);
            }
            // send get request
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url + key);
            Console.WriteLine("[*] Checking key...");
            request.AutomaticDecompression = DecompressionMethods.GZip;
            
            try
            {
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                using (Stream stream = response.GetResponseStream())
                using (StreamReader reader = new StreamReader(stream))
                {
                    string? result = reader.ReadToEnd();
                    
                    if (result == "None")
                    {
                        Console.WriteLine("[*] Key is valid.");
                        File.WriteAllText(path + "\\key.txt", key);
                        Console.WriteLine("[*] Created key file with the key.");
                        Finished(args);
                    }
                    else
                    {
                        Console.WriteLine("[!] Key is already in use. Comparing response to HWID...\n");
                        if (result == hwid)
                        {
                            Console.WriteLine("[*] Key is valid.");
                            File.WriteAllText(path + "\\key.txt", key);
                            Console.WriteLine("[*] Created key file with the key.");
                            Finished(args);
                        }
                        else
                        {
                            Console.WriteLine("[!] Key is already in use. Please try again.\n");
                            CheckKey(args);
                        }
                    }
                }
            } catch (WebException)
            {
                Console.WriteLine("[!] An error occured while checking the key or the key is invalid. Please try again.\n");
                CheckKey(args);
            }
        }

        static void Finished(string[] args)
        {
            Console.WriteLine("[*] zBot Installation complete. Please open Geometry Dash.\n");
            Console.WriteLine("[*] Opening the game may give you a virus detection, it is a false positive and you have to whitelist it.");
            Console.WriteLine("[*] If you have any more issues or questions, please read the #faq channel in the Discord.\n");
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
            Environment.Exit(0);
        }

        CheckFree(args);
    }
}