# Cloudera QuickStart — Hadoop/Sqoop Startup Checklist

Use this every time you start the Cloudera QuickStart Docker container for Hadoop/Sqoop practicals.

**Work inside the container as the `cloudera` user.**

---

## 1. Start the required services

Copy-paste this block:

```bash
# HDFS
sudo service hadoop-hdfs-namenode restart
sudo service hadoop-hdfs-datanode restart
# Optionally
sudo service hadoop-hdfs-secondarynamenode restart

# YARN
sudo service hadoop-yarn-resourcemanager restart
sudo service hadoop-yarn-nodemanager restart

# Hue, Hue-Hive connection
sudo service hive-metastore restart
sudo service hive-server2 restart

# MySQL
sudo service mysql restart

# For sqoop Practicals, check sqoop-mysql connection
sqoop list-databases \
--connect jdbc:mysql://localhost:3306/ \
--username root \
--password cloudera
```

Wait a few seconds after the commands finish.

---

## 2. Turn off HDFS Safe Mode

Run:

```bash
hdfs dfsadmin -safemode leave
```

You can confirm:

```bash
hdfs dfsadmin -safemode get
```

Expected:

```text
Safe mode is OFF
```

---

## 3. Quick service check

Run:

```bash
sudo -u hdfs jps
sudo -u yarn jps
sudo -u hbase jps
```

You should see:

**HDFS:**

```text
NameNode
DataNode
```

**YARN:**

```text
ResourceManager
NodeManager
```

Then check HDFS:

```bash
hdfs dfs -ls /
```

If it lists the HDFS root directories, HDFS is working.

---

# One Copy-Paste Startup Block

If you want the shortest routine, run this after entering the container:

```bash
sudo service hadoop-hdfs-namenode restart
sudo service hadoop-hdfs-datanode restart
sudo service hadoop-hdfs-secondarynamenode restart
sudo service hadoop-yarn-resourcemanager restart
sudo service hadoop-yarn-nodemanager restart
sudo service mysql restart
sudo service hive-metastore restart
sudo service hive-server2 restart
sleep 5

hdfs dfsadmin -safemode leave

sudo -u hdfs jps
sudo -u yarn jps

hdfs dfs -ls /

# For sqoop Practicals, check sqoop-mysql connection
sqoop list-databases \
--connect jdbc:mysql://localhost:3306/ \
--username root \
--password cloudera
```

If:

- `NameNode` and `DataNode` appear,
- `ResourceManager` and `NodeManager` appear,
- `hdfs dfs -ls /` works,

**the environment is ready for the practical.**

---

# 3-Item Checklist

Before starting a practical, only remember:

### [ ] 1. Restart services

```bash
sudo service hadoop-hdfs-namenode restart
sudo service hadoop-hdfs-datanode restart
sudo service hadoop-hdfs-secondarynamenode restart
sudo service hadoop-yarn-resourcemanager restart
sudo service hadoop-yarn-nodemanager restart
sudo service mysql restart
sudo service hive-metastore restart
sudo service hive-server2 restart
```

### [ ] 2. Leave Safe Mode

```bash
hdfs dfsadmin -safemode leave
```

### [ ] 3. Verify

```bash
sudo -u hdfs jps
sudo -u yarn jps
hdfs dfs -ls /
```

For Sqoop practicals, additionally test:

```bash
sqoop list-databases \
--connect jdbc:mysql://localhost:3306/ \
--username root \
--password cloudera
```

---

## If Something Still Fails

Do not immediately rerun the whole practical.

Use these targeted fixes:

### Sqoop says ResourceManager cannot be reached

```bash
sudo service hadoop-yarn-resourcemanager restart
sudo service hadoop-yarn-nodemanager restart
```

Then:

```bash
sudo -u yarn jps
```

### Sqoop says HDFS is in Safe Mode

```bash
hdfs dfsadmin -safemode leave
```

### MySQL connection fails

```bash
sudo service mysql restart
```

Then test:

```bash
mysql -u root -p
```

Password:

```text
cloudera
```

### HDFS commands fail

```bash
sudo service hadoop-hdfs-namenode restart
sudo service hadoop-hdfs-datanode restart
```

Then:

```bash
hdfs dfs -ls /
```

### Hive commands fail in the Hue WebUI

```bash
sudo service hive-metastore restart
sudo service hive-server2 restart
```

---

## Important Details for Your Labs

| Item | Value |
|---|---|
| Normal user | `cloudera` |
| HDFS service user | `hdfs` |
| YARN service user | `yarn` |
| MySQL user | `root` |
| MySQL password | `cloudera` |
| MySQL port | `3306` |
| Sqoop version | `1.4.6-cdh5.7.0` |
| Hadoop version | `2.6.0-cdh5.7.0` |

Use `cloudera` for normal practical commands. Use `sudo -u hdfs jps` and `sudo -u yarn jps` only for checking the corresponding service processes.
