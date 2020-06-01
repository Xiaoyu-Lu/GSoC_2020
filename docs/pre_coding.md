GSoC 2020: Age Group Prediction in Images & Audio

# Pre-Coding Phase

Before June 1st

## Community Bonding:

### software set-up

1. Access the CWRU via VPN. 

   > Access to the CWRU is restricted only to Campus network or through VPN (vpnsetup.case.edu), if connecting from outside campus.

   I wrote a [walk-through](https://sites.google.com/case.edu/techne-public-site/cwru-hpc-orientation/access-cwru-hpc-via-vpn?authuser=0) and pulished on Redhen Techne Site.

2. Prepare for working on gallina

   > “gallina” is a Red Hen Lab file server mounted on CWRU HPC

   1. Log in

      Open your terminal, enter:

      ```shell
      $ ssh <your_username>@rider.case.edu
      ```

      Then, it shows something like `Are you sure you want to continue connecting (yes/no)?` . You should enter `yes`.

      ```shell
      Are you sure you want to continue connecting (yes/no)? yes
      Warning: Permanently added 'rider.case.edu,1234567' (ECDSA) to the list of known hosts.
      ```

      It will require your password:

      ```shell
      <your_username>@rider.case.edu's password:<your_password>
      ```

      Then, you are logged in!

      ```shell
      [<your_username>@hpc3 ~]$ 
      ```

   2. add RSA

      Check your current path, you should in your home directory:

      ```shell
      [<your_username>@hpc3 ~]$ pwd
      /home/<your_username>
      ```

      - using username `abc123` as an example:

        ```shell
        [abc123@hpc3 ~]$ pwd
        /home/abc123
        ```

      Make `.ssh` directory:

      ```shell
      $ mkdir .ssh
      ```

      Open it:

      ```shell
      $ cd .ssh
      ```

      Creat a new file `authorized_keys`:

      ```shell
      $ touch authorized_keys
      ```

      Open this file:

      ```shell
      $ nano authorized_keys
      ```

      Copy paste the RSA key into the file:

      ```
      ssh-rsa ....
      ```

      Save and exit the file.

   3. **Create your own directory in gallina home**

      Naviagate to the gallina home

      ```shell
      $ cd /mnt/rds/redhen/gallina/home/
      ```

      Make your own directory:

      ```shell
      $ mkdir <your_username>
      ```

      Check the file permissions:

      ```shell
      $ ls -al <your_username>
      ```

      - using username `abc123` as an example:

        ```shell
        $ ls -al abc123
        total 20
        drwxr-sr-x  2 abc123 mbt8  2 May 10 16:47
        ```

        It should be `drwxrwsr-x`. So we change it to 2775:

        ```shell
        $ chmod 2775 <your_username>
        ```

3. [Singularity](https://sites.google.com/case.edu/techne-public-site/singularity?authuser=0)

   1. install Singularity
   2. build a recipe and push on your GitHub repo
   3. build new container by clicking `ADD A COLLECTION `  on [Singluarity-hub My Collections page](https://singularity-hub.org/collections/my)

   4. push == automatically build



