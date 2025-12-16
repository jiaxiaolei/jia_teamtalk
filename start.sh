
#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
# ✅ 直接运行 Python 脚本，触发 uvicorn.run(..., log_config=...)
python src/app/main.py --port=8002

#或者
#uvicorn app.main:app --reload --app-dir src --port=8002
