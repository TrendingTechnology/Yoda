# 📦 Yoda ⛏

**Yoda**
A CLI that takes away the hassle of managing your submission files on different online-judges by
automating the entire process of collecting and organizing your code submissions in one single Directory on your Machine also it distils User Submissions into beautiful Submission HeatMap.

## Highlights
* Downloads your AC solutions from CodeForces,CodeChef and Atcoder and creates a Directory within your Home Directory with the following File Structure:
Contests  
   ├── Codeforces  
        |──<Handle-Name>  
                ├── <Contest-ID>  
                        |── <problem-index>  
        |──<tourist>  
                └── 592  
                    └── A.cpp  
    ├── CodeChef   
        |──<Handle-Name>  
                ├── <Contest-Name>  
                        |── <problem-name>  
                            └──<problem>  
        |──<tourist>  
                └── AUG20B  
                    └──CHEFWED  
                            └──CHEFWED.cpp   
    ├── AtCoder  
        |──<Handle-Name>  
                ├── <Contest-Name>  
                        |── <problem-level>  
        |──<tourist>  
                └── AtCoder Beginner Contest 230  
                    └── A.cpp  
* Supports both Linux and Windows , see [Releases](https://github.com/NikharManchanda/Yoda/releases/tag/Yoda). 
* Fully automated collection of all yours submissions with minimal effort setup
* Simple and easy and pleasing interface to use interface to get you started in minutes
* Extensive traceability for your submissions for Each OJ , Contest Name , Problem Name with the problem file stored with proper language extension.
* Provides Clear and Beautiful Submission Heatmap of your Accepted Solutions for each Online Judge
 for all three OJ's even Atcoder , CodeChef doesn't provide it 😉.

## Platforms

Harwest currently has extensive support for the following platforms:
* [Codeforces](https://codeforces.com/)
* [AtCoder](https://atcoder.jp/)
* [CodeChef](https://www.codechef.com/)

While integration with various other OJs are still in the kitchen , your Contributions are always welcomed 😄.


## Installation

1.) You will require `Python 3.5+` along with `pip3` in order to be able to install and use Yoda.
Refer to the documentation for installing `pip` on [windows](https://phoenixnap.com/kb/install-pip-windows), 
[ubuntu/linux](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) or
[macOS](https://docs.python-guide.org/starting/install3/osx/)

2.) Install this Github Repository and then enter into that directory in the terminal/command prompt then paste the follwing command:
```bash
$ pip install -e .
```

## Getting Started

After installing the package, run the following command in the terminal:
```bash
$ yoda
```
You'd be greeted with something like this:
```bash
mn@pop-os:~$ yoda

...:██╗░░░██╗░█████╗░██████╗░░█████╗░:...
...:╚██╗░██╔╝██╔══██╗██╔══██╗██╔══██╗:...
...:░╚████╔╝░██║░░██║██║░░██║███████║:...
...:░░╚██╔╝░░██║░░██║██║░░██║██╔══██║:...
...:░░░██║░░░╚█████╔╝██████╔╝██║░░██║:...
...:░░░╚═╝░░░░╚════╝░╚═════╝░╚═╝░░╚═╝:...
    
    Hey there! 👋 Looks like you're using Yoda for the first time. Let's get you started 🚀
    There are three differnet OJ's from which you can get your User Statistics:
    Atcoder
    CodeForces
    CodeChef
    For each one of the OJ's you can Download all your AC solutions ✅ as well as Submission Heatmap for each of the Website!!
    🥳 You rock! We're good to go now 🥳
```
To use it for a particular OJ run
```bash
$ yoda <platform> 
$ yoda codeforces  # example
```

Now comes the main part :
1.)To harvest your submissions from the Codeforces platform.
Type the following command:
```bash
$ yoda <platform> <command>
$ yoda codeforces download  # example
```

You'll be prompted for providing your Codeforces handle name
```bash
> Enter your prestigious Codeforces Handle : tourist
```

Yoda will then start scraping all your AC submissions, starting from most recent submission till your very first submission.

2.) Get your Submisssion HeatMap:

Type the following command:

```bash
$ yoda <platform> <command>
$ yoda codeforces graph  # example
```

You'll be prompted for providing your Codeforces handle name

```bash
> Enter your prestigious Codeforces Handle : tourist
```

Yoda will then output on a new window your Submission HeatMap !!.

## License

[MIT License](https://github.com/NikharManchanda/Yoda/blob/main/LICENSE)
