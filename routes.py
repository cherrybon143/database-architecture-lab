from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, init_db